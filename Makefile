PYTHON = python3

help:
	@echo "Available commands :"
	@echo "install"
	@echo "lint"
	@echo "run"
	@echo "clean"

run:
	@python3 a_maze_ing.py config.txt

lint:
	@flake8

clean:
	@rm -rf mazegen/__pycache__

install:
	python -m pip install mypy



###add mypy and virtual env