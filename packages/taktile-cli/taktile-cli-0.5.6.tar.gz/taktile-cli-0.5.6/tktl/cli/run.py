import click

from tktl.cli.common import get_secrets
from tktl.commands.run import run_container


@click.command()
@click.option(
    "--path",
    "-p",
    help="Directory where the deployment lives",
    required=False,
    default=".",
)
@click.option(
    "--secrets-repository",
    "-s",
    help="Full repository name (owner/name) to use from which to get the secret names",
    required=False,
)
@click.option(
    "--nocache/--cache",
    help="Enable or disable using cache of images",
    is_flag=True,
    default=False,
)
@click.option("--background", help="Run the image in the background", is_flag=True)
@click.option(
    "--auth/--no-auth",
    help="Run with auth enabled or disabled. Enabled by default",
    default=True,
)
@click.option(
    "--color/--no-color",
    help="Enable or disable colored output",
    is_flag=True,
    default=True,
)
def run(
    path: str,
    nocache: bool,
    background: bool,
    auth: bool,
    color: bool,
    secrets_repository: str,
) -> None:
    """
    Run a deployment locally

    Parameters
    ----------
    auth
    background
    nocache
    path
    color
    secrets_repository

    Returns
    -------

    """
    secrets = get_secrets(secrets_repository=secrets_repository)
    run_container(
        path=path,
        nocache=nocache,
        background=background,
        auth_enabled=auth,
        color_logs=color,
        secrets=secrets,
    )
