"""Shared command options."""

import logging
from enum import Enum
from functools import wraps
from typing import Any, Callable

from click import BadParameter, Choice, option

MAX_VERBOSITY_LEVEL = 2
logger = logging.getLogger(__name__)


class OutputFormat(Enum):

    """Represents the available output formats for data."""

    JSON = "json"
    CSV = "csv"


def output_format_option(f: Callable[..., Any]) -> Callable[..., Any]:
    """Add an output format option to a command-line interface function.

    This decorator modifies a function to add an option allowing users to specify the desired output format.
    """
    return option(
        "-o",
        "--output",
        default=OutputFormat.CSV.value,
        type=Choice([e.value for e in OutputFormat], case_sensitive=False),
        help="Specify the output format; valid options are json or csv, default is csv.",
    )(f)


def get_logging_level(verbosity_level: int) -> int:
    """Calculate the logging level based on the provided verbosity level.

    The higher the verbosity level, the lower the logging level. This means that higher verbosity levels result in more detailed logging.
    """
    return logging.WARNING - (10 * verbosity_level)


def setup_logging(level: int) -> None:
    """Configure the logging settings."""
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def validate_verbose(ctx: Any, param: Any, value: Any) -> int:
    """Validate the verbosity level."""
    if not isinstance(value, int):
        raise BadParameter("invalid verbosity level type")

    if 0 <= value <= MAX_VERBOSITY_LEVEL:
        return value

    raise BadParameter(f"the permitted range for the verbosity level is from 0 to 2, found {value}")


def verbose_option(cmd: Callable[..., Any]) -> Callable[..., Any]:
    """Add a verbose option to a command-line interface function.

    This decorator ensures that the logging level is set based on the verbosity level specified by the user.
    """

    @option(
        "-v",
        "--verbose",
        count=True,
        callback=validate_verbose,
        help="Increase verbosity level; use multiple times for more verbosity, max 2 times.",
    )
    @wraps(cmd)
    def _verbose_option(*args: Any, **kwargs: Any) -> Any:
        setup_logging(get_logging_level(kwargs.pop("verbose", False)))

        return cmd(*args, **kwargs)

    return _verbose_option
