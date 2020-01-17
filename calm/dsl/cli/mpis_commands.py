import json
import click

from calm.dsl.api import get_api_client

from .utils import highlight_text
from .main import get, describe, launch
from .mpis import get_published_mpis, get_app_family_list, describe_mpi, launch_mpi


def _get_app_family_list():
    """adds the 'All' option to categories"""

    categories = get_app_family_list()
    categories.append("All")
    return categories


@get.command("mpis")
@click.option("--name", "-n", default=None, help="Search for mpis by name")
@click.option("--quiet", "-q", is_flag=True, default=False, help="Show only mpi names.")
@click.option(
    "--app_family",
    "-a",
    type=click.Choice(_get_app_family_list()),
    default="All",
    help="App Family Category for mpi",
)
@click.option(
    "--display_all",
    "-d",
    is_flag=True,
    default=False,
    help="Show all mpis with any version",
)
@click.pass_obj
def _get_mpis(obj, name, quiet, app_family, display_all):
    get_published_mpis(name, quiet, app_family, display_all)


@describe.command("mpi")
@click.argument("mpi_name")
@click.option("version", "-v", default=None, help="Version of MPI")
@click.pass_obj
def _describe_mpi(obj, mpi_name, version):
    """Describe a market place item"""

    describe_mpi(mpi_name, version)


@launch.command("mpi")
@click.argument("mpi_name")
@click.option("--version", "-v", default=None, help="Version of MPI")
@click.option("--project", "-pj", default=None, help="Project for the application")
@click.option("--app_name", "-a", default=None, help="Name of your app")
@click.option(
    "--profile_name",
    "-p",
    default=None,
    help="Name of app profile to be used for blueprint launch",
)
@click.option(
    "--ignore_runtime_variables",
    "-i",
    is_flag=True,
    default=False,
    help="Ignore runtime variables and use defaults",
)
@click.pass_obj
def _launch_mpi(
    obj, mpi_name, version, project, app_name, profile_name, ignore_runtime_variables,
):
    """Launch a market place blueprint"""

    launch_mpi(
        mpi_name=mpi_name,
        version=version,
        project=project,
        app_name=app_name,
        profile_name=profile_name,
        patch_editables=not ignore_runtime_variables,
    )