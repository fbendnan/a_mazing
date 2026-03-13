PYTHON = python3
MAIN = main.py
CONFIG_FILE = config.txt

help:
	@echo "Available commands:"
	@echo " install      Install project dependencies"
	@echo " run          Run the maze program"
	@echo " lint         Run mypy checks"
	@echo " lint-strict  Run flake8 and strict mypy"
	@echo " debug        Run program with debugger"
	@echo " build        Build wheel package"
	@echo " clean        Remove cache and build files"

run:
	$(PYTHON) $(MAIN) $(CONFIG_FILE)

lint:
	$(PYTHON) -m mypy . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install flake8 mypy build
	$(PYTHON) -m pip install ./mazegen-1.0.0-py3-none-any.whl

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG_FILE)

build:
	$(PYTHON) -m build --wheel

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf mazegen/__pycache__
	rm -rf maze_help/__pycache__
	find . -name "*.pyc" -delete
	rm -rf dist
	rm -rf maze.txt

.PHONY: help install run clean debug lint lint-strict build