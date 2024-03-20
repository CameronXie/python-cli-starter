# Docker
.PHONY: up
up:
	@docker compose up --build -d

.PHONY: down
down:
	@docker compose down -v

# CI/CD
.PHONY: ci-%
ci-%:
	@docker compose run --rm dev sh -c 'make $*'

# Dev
.PHONY: test
test: test-py

.PHONY: build
build: test-py
	@poetry build

.PHONY: test-py
test-py: full-install type-py lint-py unit-py

.PHONY: lint-py
lint-py:
	@# run both ruff format and lint. https://github.com/astral-sh/ruff/issues/8232
	@poetry run ruff format .
	@poetry run ruff check .

.PHONY: type-py
type-py:
	@poetry run mypy -v .

.PHONY: unit-py
unit-py:
	@poetry run pytest

.PHONY: full-install
full-install:
	@poetry install
