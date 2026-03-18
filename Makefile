VENV := .venv
PYTHON := $(VENV)/bin/python3
UV := uv
PROG := fly_in.py
SRCFILES := fly_in.py \
	simulation_engine.py \
	field_class.py \
	errors.py \
	colors.py \

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Run the application"
	@echo "  make clean       - Clean temporary files"
	@echo "  make lint        - Run linters and type checkers"
	@echo "  make lint-strict - Run linters and type checkers in strict mode"

install:
	@$(UV) sync

run:
	@$(UV) run $(PYTHON) $(PROG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-all: clean
	rm -rf $(VENV)

lint:
	$(UV) run $(PYTHON) -m flake8 $(SRCFILES)
	$(UV) run $(PYTHON) -m mypy $(SRCFILES) \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs \

lint-strict:
	$(UV) run $(PYTHON) -m flake8 $(SRCFILES)
	$(UV) run $(PYTHON) -m mypy $(SRCFILES) --strict

test:
	$(UV) run pytest

.PHONY: help install run clean lint lint-strict
