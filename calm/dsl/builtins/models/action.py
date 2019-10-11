import ast
import inspect
import uuid

from .entity import EntityType, Entity
from .descriptor import DescriptorType
from .validator import PropertyValidator
from .task import dag, create_call_rb
from .runbook import runbook_create
from .node_visitor import GetCallNodes

# Action - Since action, runbook and DAG task are heavily coupled together,
# the action type behaves as all three.


class ActionType(EntityType):
    __schema_name__ = "Action"
    __openapi_type__ = "app_action"

    def __call__(cls, name=None):
        return create_call_rb(cls.runbook, name=name) if cls.runbook else None

    def assign_targets(cls, parent_entity):
        for task in cls.runbook.tasks:
            if not task.target_any_local_reference:
                task.target_any_local_reference = parent_entity.get_task_target()


class ActionValidator(PropertyValidator, openapi_type="app_action"):
    __default__ = None
    __kind__ = ActionType


def _action(**kwargs):
    name = getattr(ActionType, "__schema_name__")
    bases = (Entity,)
    return ActionType(name, bases, kwargs)


Action = _action()


def _action_create(**kwargs):
    name = str(uuid.uuid4())[:8] + "_" + getattr(ActionType, "__schema_name__")
    name = kwargs.get("name", kwargs.get("__name__", name))
    bases = (Action,)
    return ActionType(name, bases, kwargs)


class action(metaclass=DescriptorType):
    """
    action descriptor
    """

    def __init__(self, user_func):
        """
        A decorator for generating actions from a function definition.
        Args:
            user_func (function): User defined function
        Returns:
            (Action): Action class
        """

        # Generate the entity names
        self.action_name = user_func.__name__
        self.action_description = user_func.__doc__ or ""
        self.runbook_name = str(uuid.uuid4())[:8] + "_runbook"
        self.dag_name = str(uuid.uuid4())[:8] + "_dag"
        self.user_func = user_func
        self.user_runbook = runbook_create(**{"name": self.runbook_name})
        self.__parsed__ = False

    def __call__(self, name=None):
        return create_call_rb(self.user_runbook, name=name)

    def __get__(self, instance, cls):
        """
        Translate the user defined function to an action.
        Args:
            instance (object): Instance of cls
            cls (Entity): Entity that this action is defined on
        Returns:
            (ActionType): Generated Action class
        """
        if cls is None:
            return self

        if self.__parsed__:
            return self.user_action

        # Get the source code for the user function.
        # Also replace tabs with 4 spaces.
        src = inspect.getsource(self.user_func).replace("\t", "    ")

        # Get the indent since this decorator is used within class definition
        # For this we split the code on newline and count the number of spaces
        # before the @action decorator.
        # src = "    @action\n    def action1():\n    CalmTask.Exec.ssh("Hello World")"
        # The indentation here would be 4.
        padding = src.split("\n")[0].rstrip(" ").split(" ").count("")

        # This recreates the source code without the indentation and the
        # decorator.
        new_src = "\n".join(line[padding:] for line in src.split("\n")[1:])

        # Get all the child tasks by parsing the source code and visiting the
        # ast.Call nodes. ast.Assign nodes become variables.
        node = ast.parse(new_src)
        func_globals = self.user_func.__globals__.copy()
        node_visitor = GetCallNodes(func_globals, target=cls.get_task_target())
        try:
            node_visitor.visit(node)
        except Exception as ex:
            self.__exception__ = ex
            raise
        tasks, variables, task_list = node_visitor.get_objects()
        edges = []
        for from_tasks, to_tasks in zip(task_list, task_list[1:]):
            if not isinstance(from_tasks, list):
                from_tasks = [from_tasks]
            if not isinstance(to_tasks, list):
                to_tasks = [to_tasks]
            for from_task in from_tasks:
                for to_task in to_tasks:
                    edges.append((from_task.get_ref(), to_task.get_ref()))

        # First create the dag
        self.user_dag = dag(
            name=self.dag_name,
            child_tasks=tasks,
            edges=edges,
            target=cls.get_task_target()
            if getattr(cls, "__has_dag_target__", True)
            else None,
        )

        # Modify the user runbook
        self.user_runbook.main_task_local_reference = self.user_dag.get_ref()
        self.user_runbook.tasks = [self.user_dag] + tasks
        self.user_runbook.variables = [variable for variable in variables.values()]

        # System action names
        action_name = self.action_name
        ACTION_TYPE = "user"
        func_name = self.user_func.__name__.lower()
        if func_name.startswith("__") and func_name.endswith("__"):
            SYSTEM = getattr(cls, "ALLOWED_SYSTEM_ACTIONS", {})
            FRAGMENT = getattr(cls, "ALLOWED_FRAGMENT_ACTIONS", {})
            if func_name in SYSTEM:
                ACTION_TYPE = "system"
                action_name = SYSTEM[func_name]
            elif func_name in FRAGMENT:
                ACTION_TYPE = "fragment"
                action_name = FRAGMENT[func_name]

        # Finally create the action
        self.user_action = _action_create(
            **{
                "name": action_name,
                "description": self.action_description,
                "critical": ACTION_TYPE == "system",
                "type": ACTION_TYPE,
                "runbook": self.user_runbook,
            }
        )

        self.__parsed__ = True

        return self.user_action


class parallel:
    __calm_type__ = "parallel"
