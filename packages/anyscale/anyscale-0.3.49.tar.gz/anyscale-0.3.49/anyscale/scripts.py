import json
import logging
import os
import sys
from typing import Any

import click
from packaging import version

from anyscale.api import instantiate_api_client
from anyscale.client.openapi_client.rest import ApiException  # type: ignore
from anyscale.commands.anyscale_api.api_commands import anyscale_api
from anyscale.commands.cloud_commands import cloud_cli
from anyscale.commands.exec_commands import anyscale_exec
from anyscale.commands.list_commands import list_cli
from anyscale.commands.project_commands import anyscale_clone, anyscale_init
from anyscale.commands.session_commands import (
    anyscale_autopush,
    anyscale_autosync,
    anyscale_fork,
    anyscale_pull,
    anyscale_push,
    anyscale_ssh,
    anyscale_stop,
    anyscale_up,
)
from anyscale.commands.session_commands_hidden import (
    anyscale_start,
    session_cli,
)
from anyscale.commands.snapshot_commands_hidden import snapshot_cli
import anyscale.conf


logger = logging.getLogger(__file__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

if anyscale.conf.AWS_PROFILE is not None:
    logger.info("Using AWS profile %s", anyscale.conf.AWS_PROFILE)
    os.environ["AWS_PROFILE"] = anyscale.conf.AWS_PROFILE


class AliasedGroup(click.Group):
    # This is from https://stackoverflow.com/questions/46641928/python-click-multiple-command-names
    def get_command(self, ctx: Any, cmd_name: str) -> Any:
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
    cls=AliasedGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option(
    "--version",
    "-v",
    "version_flag",
    is_flag=True,
    default=False,
    help="Current anyscale version.",
)
@click.option(
    "--json",
    "show_json",
    is_flag=True,
    default=False,
    help="Return output as json, for use with --version.",
)
@click.pass_context
def cli(ctx: Any, version_flag: bool, show_json: bool) -> None:

    # Use anyscale vendored Ray for the CLI:
    sys.path.insert(0, anyscale.ANYSCALE_RAY_DIR)

    try:
        api_client = instantiate_api_client(no_cli_token=True)
        resp = api_client.get_anyscale_version_api_v2_userinfo_anyscale_version_get()
        curr_version = anyscale.__version__
        latest_version = resp.result.version
        if version.parse(curr_version) < version.parse(latest_version):
            message = "Warning: Using version {0} of anyscale. Please update the package using pip install anyscale -U to get the latest version {1}".format(
                curr_version, latest_version
            )
            print("\033[91m{}\033[00m".format(message), file=sys.stderr)
    except ApiException as e:
        logger.warning(
            "Error {} while trying to get latest anyscale version number: {}".format(
                e.status, e.reason
            )
        )
    except Exception as e:
        logger.warning(e)

    if version_flag:
        ctx.invoke(version_cli, show_json=show_json)


@click.command(name="version", help="Display version of the anyscale CLI.")
@click.option(
    "--json", "show_json", is_flag=True, default=False, help="Return output as json."
)
def version_cli(show_json: bool) -> None:
    if show_json:
        print(json.dumps({"version": anyscale.__version__}))
    else:
        print(anyscale.__version__)


@cli.command(
    name="help", help="Display help documentation for anyscale CLI.", hidden=True
)
@click.pass_context
def anyscale_help(ctx: Any) -> None:
    # TODO: Remove after we no longer want this announcement (in a few weeks).
    announcement = (
        "Anyscale now runs on Ray version 1.0.1. Please make sure to have "
        "this version of Ray installed locally, and in all future sessions "
        "with Anyscale. Any new sessions started will automatically be started "
        "with the correct Ray version, but any sessions started before November "
        " 13, 2020 may need to be restarted or updated with Ray 1.0.1."
        "You can check your local Ray version with: "
        "    $ ray --version"
    )
    print("\033[32m{}\033[00m".format(announcement), file=sys.stderr)
    print(ctx.parent.get_help())


cli.add_command(session_cli)
cli.add_command(snapshot_cli)
cli.add_command(cloud_cli)
cli.add_command(version_cli)
cli.add_command(list_cli)

cli.add_command(anyscale_init)
cli.add_command(anyscale_start)
cli.add_command(anyscale_up)
cli.add_command(anyscale_stop)
cli.add_command(anyscale_autosync)
cli.add_command(anyscale_autopush)
cli.add_command(anyscale_fork)
cli.add_command(anyscale_clone)
cli.add_command(anyscale_ssh)
cli.add_command(anyscale_exec)
cli.add_command(anyscale_pull)
cli.add_command(anyscale_push)
cli.add_command(anyscale_help)

# Commands to interact with the Anyscale API
cli.add_command(anyscale_api)

ALIASES = {"h": anyscale_help}


def main() -> Any:
    return cli()


if __name__ == "__main__":
    main()
