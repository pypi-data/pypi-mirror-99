import click
from alfa_sdk.common.stores import AuthStore, ConfigStore
from alfa_sdk.common.exceptions import AuthenticationError
from alfa_cli.common.click import BaseCliCommand
from alfa_cli.common.factories import create_session
from alfa_cli.common.utils import get_short_environment_name


@click.command(cls=BaseCliCommand)
@click.option("--alfa-id", help="ALFA Instance ID [env=ALFA_ID]", envvar="ALFA_ID")
@click.option("--region", help="ALFA Region [env=PLATFORM_REGION]", envvar="PLATFORM_REGION")
@click.option(
    "-ci", "--client-id", help="ALFA Client ID [env=ALFA_CLIENT_ID]", envvar="ALFA_CLIENT_ID"
)
@click.option(
    "-cs",
    "--client-secret",
    help="ALFA Client Secret [env=ALFA_CLIENT_SECRET]",
    envvar="ALFA_CLIENT_SECRET",
)
@click.option("--verbose/--no-verbose", help="(dev) Default verbosity of outputs")
@click.option("--alfa-env", help="(dev) Environment of ALFA to connect to.")
@click.pass_obj
def configure(obj, alfa_id, region, client_id, client_secret, verbose, alfa_env):
    """Configure ALFA CLI options.

    If this command is run with no arguments, and the fallback environment
    variables are not defined, you will be prompted for configuration values.
    The options will be stored inside '~/.config/alfa/'.

    '(dev)' indicates options which are intended for internal developers.
    There are no prompts for these options."""

    store = AuthStore.get_group()

    # Auth

    prev_client_id = store.get("client_id", None)
    prev_client_secret = store.get("client_secret", None)

    if not client_id:
        client_id = click.prompt("ALFA Client ID", type=str, default=prev_client_id)
    if not client_secret:
        client_secret = click.prompt("ALFA Client Secret", type=str, default=prev_client_secret)

    AuthStore.purge()
    AuthStore.set_values({"client_id": client_id, "client_secret": client_secret})

    # Config

    prev_alfa_id = store.get("alfa_id", 'public')
    prev_region = store.get("platform_region", 'eu-central-1')

    if alfa_env:
        ConfigStore.set_value("alfa_env", get_short_environment_name(alfa_env), group="alfa")
    ConfigStore.set_value("alfa_id", alfa_id or prev_alfa_id, group="alfa")
    ConfigStore.set_value("platform_region", region or prev_region, group="alfa")

    if verbose is not None:
        ConfigStore.set_value("verbose", verbose)

    # Output

    try:
        session = create_session(alfa_env=alfa_env)
        return obj["logger"].result({"message": "Authentication success!", "user": session.auth.user})
    except AuthenticationError:
        AuthStore.set_values({"client_id": prev_client_id, "client_secret": prev_client_secret})
        raise
