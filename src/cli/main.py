"""DNS CLI root command and bootstrap."""

from importlib.metadata import version

from click import group, version_option

from .dns_lookup_cmd import dns_lookup

MODULE_NAME = "cli_starter"


@group(
    commands={
        "lookup": dns_lookup,
    }
)
@version_option(version=version(MODULE_NAME))
def cli() -> None:
    """DNS CLI."""
