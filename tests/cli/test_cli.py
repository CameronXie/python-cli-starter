"""CLI Tests."""

import logging
import socket
from typing import ClassVar
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from cli.main import cli


class TestCLI:

    """Test CLI."""

    resolved_ips: ClassVar[dict] = ["127.0.0.1", "127.0.0.2"]

    lookup_success_cases: ClassVar[dict] = {
        "return resolved ips in csv": (["-o", "csv"], None, "127.0.0.1,127.0.0.2\n"),
        "return resolved ips from specific port number in json format": (
            ["-o", "json", "-p", 1234],
            1234,
            '["127.0.0.1", "127.0.0.2"]\n',
        ),
        "return resolved ips in csv as default and increase verbosity level to debug": (
            ["-vv"],
            None,
            "127.0.0.1,127.0.0.2\n",
        ),
    }

    @pytest.mark.parametrize(
        "opts,port,expected_output",
        lookup_success_cases.values(),
        ids=lookup_success_cases.keys(),
    )
    @patch("socket.getaddrinfo")
    def test_cli_lookup_success(
        self,
        mock_getaddrinfo,
        opts: list[str],
        port: int | None,
        expected_output: str,
    ):
        """Test DNS lookup success cases."""
        domain = "example.com"
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (ip, 0)) for ip in self.resolved_ips
        ]
        runner = CliRunner()
        result = runner.invoke(cli, ["lookup", *opts, domain])

        assert result.exit_code == 0
        assert result.output == expected_output
        mock_getaddrinfo.assert_called_once_with(domain, port=port)

    lookup_error_cases: ClassVar[dict] = {
        "return error if domain is missing": ([], "Error: Missing argument 'DOMAIN'."),
        "return error if domain is invalid": (
            ["invalid-domain"],
            "Error: Invalid value for 'DOMAIN': value invalid-domain is not a valid domain",
        ),
        "return error if verbosity level is invalid": (
            ["-vvv", "example.com"],
            "Error: Invalid value for '-v' / '--verbose': the permitted range for the verbosity level is from 0 to 2, found 3",
        ),
    }

    @pytest.mark.parametrize(
        "args,expected_output",
        lookup_error_cases.values(),
        ids=lookup_error_cases.keys(),
    )
    @patch("socket.getaddrinfo")
    def test_cli_lookup_error(self, mock_getaddrinfo, args: list[str], expected_output: str | None):
        """Test DNS lookup error cases."""
        error_code = 2
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (ip, 0)) for ip in self.resolved_ips
        ]
        runner = CliRunner()
        result = runner.invoke(cli, ["lookup", *args])

        assert result.exit_code == error_code
        assert expected_output in result.output

    lookup_logging_cases: ClassVar[dict] = {
        "set logging format and info level": (
            ["-v"],
            {
                "format": "%(asctime)s %(message)s",
                "level": logging.INFO,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        ),
        "set logging format and debug level": (
            ["-vv"],
            {
                "format": "%(asctime)s %(message)s",
                "level": logging.DEBUG,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        ),
    }

    @pytest.mark.parametrize(
        "opts,expected_config",
        lookup_logging_cases.values(),
        ids=lookup_logging_cases.keys(),
    )
    @patch("socket.getaddrinfo")
    @patch("logging.basicConfig")
    def test_cli_lookup_logging(self, mock_config, mock_getaddrinfo, opts: list[str], expected_config: dict):
        """Test DNS Lookup log."""
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (ip, 0)) for ip in self.resolved_ips
        ]
        runner = CliRunner()
        runner.invoke(cli, ["lookup", *opts, "example.com"])
        mock_config.assert_called_once_with(**expected_config)
