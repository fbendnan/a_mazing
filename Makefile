PYTHON = python3
MAIN = a_maze_ing.py
CONFIG_FILE = config.txt

help:
	@echo "Available commands :"
	@echo "install"
	@echo "lint"
	@echo "run"
	@echo "clean"
	@echo "debug"
	@echo "lint-strict"

run:
	@python3 $(MAIN) $(CONFIG_FILE)

lint:
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@find . -name "*.pyc" -delete

install:
	@pip install flake8 mypy

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG_FILE)

lint-strict:
	@flake8 .
	@mypy . --strict

.PHONY: help install run clean debug lint lint-strict
