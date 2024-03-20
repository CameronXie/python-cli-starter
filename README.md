# CLI Starter

[![Test](https://github.com/CameronXie/python-cli-starter/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/CameronXie/python-cli-starter/actions/workflows/test.yaml)

This project aims to serve as a practical example of how to build a Command Line Interface (CLI) in Python by showcasing
a DNS CLI tool.

## Usage

This project can be easily installed using `pipx`. Execute the following command:

```shell
pipx install git+https://github.com/CameronXie/python-cli-starter.git
```

This command will add a `dnskit` CLI (Command Line Interface) application to your system.

Alternatively, you can directly run the `dnskit` CLI application using `pipx` with the following command:

```shell
pipx run --spec git+https://github.com/CameronXie/python-cli-starter.git dnskit
Usage: dnskit [OPTIONS] COMMAND [ARGS]...

  DNS CLI.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  lookup  Perform a DNS lookup and returns a list of IP addresses...
```

## Development

This project utilizes Docker to manage the local development environment. Execute the `make up` command to start the
development container.

Once inside the cli_starter_dev container, run the `poetry install` command to install all necessary dependencies. To
start the DNS CLI, you need to execute `poetry run python src/cli`.

```shell
poetry run python src/cli
Usage: cli [OPTIONS] COMMAND [ARGS]...

  DNS CLI.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  lookup  Perform a DNS lookup and returns a list of IP addresses...
```

To perform a DNS lookup, utilize the command `poetry run python src/cli lookup -vv github.com`

```shell
poetry run python src/cli lookup -vv github.com
2024-03-20 10:10:10 DNS lookup started for domain: github.com on port: None with output format: csv
<hide ip address>
```

## Build

To build the CLI, navigate to the `cli_starter_dev` container and execute the `make build` command.

## Tests

To carry out type checking, linting, and unit tests on the source code of the project, execute the `make test-py` command.
