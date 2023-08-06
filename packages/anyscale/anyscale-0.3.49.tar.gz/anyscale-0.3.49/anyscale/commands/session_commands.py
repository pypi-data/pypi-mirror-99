from typing import Any, Optional, Tuple

import click

from anyscale.controllers.project_controller import COMPUTE_CONFIG_FILENAME
from anyscale.controllers.session_controller import SessionController


@click.command(name="down", help="Stop the current session.")
@click.argument("session-name", required=False, default=None)
@click.option(
    "--workers-only", is_flag=True, default=False, help="Only destroy the workers."
)
@click.option(
    "--keep-min-workers",
    is_flag=True,
    default=False,
    help="Retain the minimal amount of workers specified in the config.",
)
@click.option("--delete", help="Delete the session as well.", is_flag=True)
@click.option(
    "--skip-snapshot", help="Skip taking snapshot.", is_flag=True, default=False,
)
@click.pass_context
def anyscale_stop(
    ctx: Any,
    session_name: Optional[str],
    workers_only: bool,
    keep_min_workers: bool,
    delete: bool,
    skip_snapshot: bool,
) -> None:
    session_controller = SessionController()
    session_controller.stop(
        session_name,
        workers_only=workers_only,
        keep_min_workers=keep_min_workers,
        delete=delete,
        skip_snapshot=skip_snapshot,
    )


@click.command(
    name="up",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start or update a session based on the current project configuration.",
)
@click.argument("session-name", required=False)
@click.option(
    "--dangerously-set-build-id",
    hidden=True,
    help="Dangerously set the build-id. This is only used by anyscale connect.",
    default=None,
)
@click.option(
    "--config", "config", help="Cluster to start session with.", default=None,
)
@click.option(
    "--build-id",
    help="The build ID generated from the app templates service.",
    # TODO: add the app templates CLI command to the description
    # once the CLI is done.
    default=None,
)
@click.option(
    "--compute-config",
    help=(
        "The JSON file of the compute config to launch this session with. "
        "An example can be found at {filename}. "
        "The full JSON schema can be viewed at {website}. ".format(
            filename=COMPUTE_CONFIG_FILENAME, website="beta.anyscale.com/ext/v0/docs",
        )
    ),
    default=None,
)
@click.option(
    "--no-restart",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip restarting Ray services during the update. "
        "This avoids interrupting running jobs."
    ),
)
@click.option(
    "--restart-only",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip running setup commands and only restart Ray. "
        "This cannot be used with 'no-restart'."
    ),
)
@click.option(
    "--min-workers",
    required=False,
    type=int,
    help="Override the configured min worker node count for the cluster.",
)
@click.option(
    "--max-workers",
    required=False,
    type=int,
    help="Override the configured max worker node count for the cluster.",
)
@click.option(
    "--disable-sync",
    is_flag=True,
    default=False,
    help=(
        "Disables syncing file mounts and project directory. This is "
        "useful when 'restart-only' is set and file syncing takes a long time."
    ),
)
@click.option("--cloud-id", required=False, help="Id of the cloud to use", default=None)
@click.option(
    "--cloud-name", required=False, help="Name of the cloud to use", default=None
)
@click.option(
    "--idle-timeout",
    required=False,
    help="Idle timeout (in minutes), after which the session is stopped. Idle "
    "time is defined as the time during which a session is not running a user "
    "command (through 'anyscale exec' or the Web UI), and does not have an "
    "attached driver. Time spent running Jupyter commands, or commands run "
    "through ssh, is still considered 'idle'. -1 means no timeout. "
    "Default: 120 minutes",
    type=int,
)
@click.option("--verbose", "-v", help="Print out more information", is_flag=True)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="DEPRECATED: Session will start without confirmation.",
)
@click.option(
    "--no-rapid-start",
    is_flag=True,
    default=False,
    help=(
        "Force bypassing RapidStart for this session. "
        "A brand new instance will be acquired from the cloud provider."
    ),
)
def anyscale_up(
    session_name: Optional[str],
    config: Optional[str],
    build_id: Optional[str],
    compute_config: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    no_restart: bool,
    restart_only: bool,
    disable_sync: bool,
    cloud_id: Optional[str],
    cloud_name: Optional[str],
    idle_timeout: Optional[int],
    verbose: bool,
    yes: bool,
    no_rapid_start: bool,
    dangerously_set_build_id: Optional[str],
) -> None:
    session_controller = SessionController()
    session_controller.up(
        session_name=session_name,
        config=config,
        build_id=build_id,
        compute_config=compute_config,
        min_workers=min_workers,
        max_workers=max_workers,
        no_restart=no_restart,
        restart_only=restart_only,
        disable_sync=disable_sync,
        cloud_id=cloud_id,
        cloud_name=cloud_name,
        idle_timeout=idle_timeout,
        verbose=verbose,
        no_rapid_start=no_rapid_start,
        dangerously_set_build_id=dangerously_set_build_id,
    )


@click.command(name="ssh", help="SSH into head node of cluster.")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option("-o", "--ssh-option", multiple=True)
def anyscale_ssh(session_name: str, ssh_option: Tuple[str]) -> None:
    session_controller = SessionController()
    session_controller.ssh(session_name, ssh_option)


@click.command(
    name="autopush",
    short_help="Automatically synchronize a local project with a session.",
    help="""
This command launches the autopush service that will synchronize
the state of your local project to the Anyscale session that you specify.

If there is only a single session running, this command without arguments will
default to that session.""",
)
@click.argument("session-name", type=str, required=False, default=None)
@click.option("--verbose", help="Show output from autopush.", is_flag=True)
@click.option(
    "-d",
    "--delete",
    help="Whether to delete the files that do not exist locally but are found in the cluster.",
    is_flag=True,
    default=False,
)
def anyscale_autopush(
    session_name: Optional[str], verbose: bool, delete: bool,
) -> None:
    session_controller = SessionController()
    session_controller.autopush(session_name, verbose, delete=delete)


@click.command(
    name="autosync",
    short_help="Automatically synchronize a local project with a session.",
    help="""
DEPRECATED: Renamed to autopush

This command launches the autosync service that will synchronize
the state of your local project with the Anyscale session that you specify.

If there is only a single session running, this command without arguments will
default to that session.""",
    hidden=True,  # HIDDEN cuz deprecated
)
@click.argument("session-name", type=str, required=False, default=None)
@click.option("--verbose", help="Show output from autosync.", is_flag=True)
@click.option(
    "-d",
    "--delete",
    help="Whether to delete the files that do not exist locally but are found in the cluster.",
    is_flag=True,
    default=False,
)
@click.option(
    "-i",
    "--ignore-errors",
    help="Whether to continue syncing even when rsync returns an error code.",
    is_flag=True,
    default=False,
)
def anyscale_autosync(
    session_name: Optional[str], verbose: bool, delete: bool, ignore_errors: bool,
) -> None:
    raise click.ClickException("Error: autosync has been renamed to autopush")


@click.command(name="push", help="Push current project to session.")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option(
    "--source",
    "-s",
    type=str,
    required=False,
    default=None,
    help="Source location of the files on the local file system which should"
    "be transferred. If source and target are specified, only those files/directories "
    "will be updated.",
)
@click.option(
    "--target",
    "-t",
    type=str,
    required=False,
    default=None,
    help="Target location on the head node to transfer the files to. If source "
    "and target are specified, only those files/directories will be updated.",
)
@click.option(
    "--config",
    type=str,
    required=False,
    default=None,
    help="Updates session with this configuration file.",
)
@click.option(
    "--all-nodes",
    "-A",
    is_flag=True,
    required=False,
    help="Choose to update to all nodes (workers and head) if source and target are specified.",
)
@click.pass_context
def anyscale_push(
    ctx: Any,
    session_name: str,
    source: Optional[str],
    target: Optional[str],
    config: Optional[str],
    all_nodes: bool,
) -> None:
    session_controller = SessionController()
    session_controller.push(session_name, source, target, config, all_nodes)


@click.command(name="pull", help="Pull session")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option(
    "--source",
    "-s",
    type=str,
    required=False,
    default=None,
    help="Source location to transfer files located on head node of cluster "
    "from. If source and target are specified, only those files/directories "
    "will be updated.",
)
@click.option(
    "--target",
    "-t",
    type=str,
    required=False,
    default=None,
    help="Local target location to transfer files to. If source and target "
    "are specified, only those files/directories will be updated.",
)
@click.option(
    "--config",
    type=str,
    required=False,
    default=None,
    help="Pulls cluster configuration from session this location.",
)
@click.confirmation_option(
    prompt="Pulling a session will override the local project directory. Do you want to continue?"
)
def anyscale_pull(
    session_name: str,
    source: Optional[str],
    target: Optional[str],
    config: Optional[str],
) -> None:
    session_controller = SessionController()
    session_controller.pull(session_name, source, target, config)


@click.command(
    name="fork", help="Clones an existing session by name and initializes it"
)
@click.argument("session-name", type=str, required=True)
@click.argument("new-session-name", type=str, required=True)
@click.option(
    "--project-name",
    type=str,
    required=False,
    default=None,
    help="""
    Name of the project the existing session belongs to.
    By default, we will use the project configured in your current workspace.
    """,
)
def anyscale_fork(
    session_name: str, new_session_name: str, project_name: Optional[str] = None
) -> None:
    session_controller = SessionController()
    output = session_controller.fork_session(session_name, new_session_name)
    print(output)
