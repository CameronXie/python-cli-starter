"""DNS Lookup Tests."""

import socket
from unittest.mock import patch

from dns.dns_lookup import get_ips


class TestDNSLookup:

    """A class that tests DNS lookup functionality."""

    @patch("socket.getaddrinfo")
    def test_get_ips(self, mock_getaddrinfo):
        """Test the get_ips method."""
        domain = "localhost"
        port = 1234
        resolved_ips = ["127.0.0.1", "127.0.0.2"]
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (ip, 0)) for ip in resolved_ips
        ]

        assert resolved_ips == get_ips(domain, port)
        mock_getaddrinfo.assert_called_once_with(domain, port=port)
