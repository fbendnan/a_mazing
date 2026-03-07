PYTHON = python3
MAIN = main.py
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
	@rm -rf mazegen/__pycache__
	@rm -rf maze_help/__pycache__
	@find . -name "*.pyc" -delete
	@rm -rf dist
	@rm -rf output_validator.py

install:
	@pip install flake8 mypy
	@pip install build
	@pip install mazegen-0.1.0-py3-none-any.whl

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG_FILE)

lint-strict:
	@flake8 .
	@mypy . --strict

build:
	python -m build --wheel

.PHONY: help install run clean debug lint lint-strict build
