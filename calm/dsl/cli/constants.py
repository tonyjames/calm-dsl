class RUNLOG:
    class STATUS:
        SUCCESS = "SUCCESS"
        PENDING = "PENDING"
        RUNNING = "RUNNING"
        FAILURE = "FAILURE"
        WARNING = "WARNING"
        ERROR = "ERROR"
        APPROVAL = "APPROVAL"
        APPROVAL_FAILED = "APPROVAL_FAILED"
        ABORTED = "ABORTED"
        ABORTING = "ABORTING"
        SYS_FAILURE = "SYS_FAILURE"
        SYS_ERROR = "SYS_ERROR"
        SYS_ABORTED = "SYS_ABORTED"
        ALREADY_RUN = "ALREADY_RUN"
        TIMEOUT = "TIMEOUT"

    TERMINAL_STATES = [
        STATUS.SUCCESS,
        STATUS.FAILURE,
        STATUS.APPROVAL_FAILED,
        STATUS.WARNING,
        STATUS.ERROR,
        STATUS.ABORTED,
        STATUS.SYS_FAILURE,
        STATUS.SYS_ERROR,
        STATUS.SYS_ABORTED,
    ]
    FAILURE_STATES = [
        STATUS.FAILURE,
        STATUS.APPROVAL_FAILED,
        STATUS.WARNING,
        STATUS.ERROR,
        STATUS.ABORTED,
        STATUS.SYS_FAILURE,
        STATUS.SYS_ERROR,
        STATUS.SYS_ABORTED,
    ]


class BLUEPRINT:
    class STATES:
        ACTIVE = "ACTIVE"
        DELETED = "DELETED"
        DRAFT = "DRAFT"
        ERROR = "ERROR"


class APPLICATION:
    class STATES:
        PROVISIONING = "provisioning"
        STOPPED = "stopped"
        RUNNING = "running"
        ERROR = "error"
        DELETED = "deleted"
        DELETING = "deleting"
        STARTING = "starting"
        STOPPING = "stopping"
        RESTARTING = "restarting"
        BUSY = "busy"
        TIMEOUT = "timeout"
        RESTARTING = "restarting"


class ACCOUNT:
    class STATES:
        DELETED = "DELETED"
        VERIFIED = "VERIFIED"
        NOT_VERIFIED = "NOT_VERIFIED"
        VERIFY_FAILED = "VERIFY_FAILED"
        DRAFT = "DRAFT"
        ACTIVE = "ACTIVE"
        UNSAVED = "UNSAVED"

    class TYPES:
        AWS = "aws"
        AHV = "nutanix"
        KUBERNETES = "k8s"
        AZURE = "azure"
        GCP = "gcp"
        VMWARE = "vmware"


class SYSTEM_ACTIONS:
    CREATE = "create"
    START = "start"
    RESTART = "restart"
    STOP = "stop"
    DELETE = "delete"
    SOFT_DELETE = "soft_delete"
