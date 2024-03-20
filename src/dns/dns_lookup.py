"""DNS Lookup Functions."""

import socket


def get_ips(domain: str, port: int | None) -> list[str]:
    """Retrieve IP addresses associated with a domain."""
    return [info[4][0] for info in socket.getaddrinfo(domain, port=port)]
