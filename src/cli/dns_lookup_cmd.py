"""DNS Lookup Command."""

import logging
import re
from typing import Any, Optional

from click import Context, Parameter, ParamType, argument, command, echo, option

from dns.dns_lookup import get_ips

from .options import OutputFormat, output_format_option, verbose_option
from .output_formatter import format_list

logger = logging.getLogger(__name__)


class DomainType(ParamType):

    """The `DomainType` class is responsible for converting and validating domain values."""

    name = "domain"

    def convert(self, value: Any, param: Optional[Parameter], ctx: Optional[Context]) -> Any:
        """Validate a provided domain string. If the domain string is valid, it is returned; else, an error is raised."""
        if not isinstance(value, str):
            self.fail(f"value {value} is not a valid string")

        if re.match(r"^((?![-_])[A-Za-z0-9-_]{0,63}(?<!-)\.)+[A-Za-z]{2,6}$", value):
            return value

        self.fail(f"value {value} is not a valid domain")


@command()
@argument("domain", type=DomainType(), nargs=1)
@option("-p", "--port", default=None, type=int, help="Port number. If not provided, defaults to None.")
@output_format_option
@verbose_option
def dns_lookup(domain: str, port: Optional[int], output: str) -> None:
    """Perform a DNS lookup and returns a list of IP addresses associated with the given domain."""
    logger.debug(f"DNS lookup started for domain: {domain} on port: {port} with output format: {output}")
    echo(format_list(get_ips(domain, port), OutputFormat(output)))
