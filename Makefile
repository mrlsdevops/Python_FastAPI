UV ?= uv

.PHONY: install test test-vv lint format ci

install:
	$(UV) sync --dev

test:
	$(UV) run pytest

test-vv:
	$(UV) run pytest -vv

lint:
	$(UV) run ruff check app tests

format:
	$(UV) run ruff format app tests

ci: lint test
