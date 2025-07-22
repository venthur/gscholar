# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif


all: lint mypy test test-release

$(VENV): pyproject.toml
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -e .['dev']
	touch $(VENV)

.PHONY: test
test: $(VENV)
	$(BIN)/pytest

.PHONY: mypy
mypy: $(VENV)
	$(BIN)/mypy

.PHONY: lint
lint: $(VENV)
	$(BIN)/ruff check .

.PHONY: build
build: $(VENV)
	rm -rf dist
	$(BIN)/python3 -m build

.PHONY: test-release
test-release: $(VENV) build
	$(BIN)/twine check dist/*

.PHONY: release
release: $(VENV) build
	$(BIN)/twine upload dist/*

.PHONY: clean
clean:
	rm -rf build dist *.egg-info
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	# coverage
	rm -rf htmlcov .coverage
