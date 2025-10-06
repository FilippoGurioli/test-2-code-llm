.PHONY: help run install install-dev test test-coverage test-watch lint format type-check security quality clean build

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip
PRE_COMMIT := $(PYTHON) -m pre_commit
RUFF := $(VENV)/bin/ruff
BLACK := $(VENV)/bin/black
MYPY := $(VENV)/bin/mypy

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

$(VENV)/bin/activate:  ## Create in-project virtual environment
	python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip setuptools wheel
	@echo "Virtual environment created in $(VENV). To activate: source $(VENV)/bin/activate"

run: $(VENV)/bin/activate  ## Run the main application
	$(PYTHON) -m t2c

install: $(VENV)/bin/activate  ## Install package in development mode
	$(PIP) install -e .

install-dev: $(VENV)/bin/activate  ## Install package and dev dependencies, install git hooks
	$(PIP) install -e ".[dev]"
	@$(PRE_COMMIT) install
	@$(PRE_COMMIT) install --hook-type commit-msg || true

test: $(VENV)/bin/activate  ## Run all tests
	$(PYTHON) -m pytest

test-coverage: $(VENV)/bin/activate  ## Run tests with coverage report
	$(PYTHON) -m pytest --cov=src/t2c --cov-report=html --cov-report=term-missing

lint: $(VENV)/bin/activate  ## Run linting (ruff)
	@$(RUFF) check src/ tests/ || true

format: $(VENV)/bin/activate  ## Format code (black + ruff)
	@$(BLACK) src/ tests/ || true
	@$(RUFF) check --fix src/ tests/ || true

type-check: $(VENV)/bin/activate  ## Run type checking (mypy)
	@$(MYPY) src/t2c/ || true

security: $(VENV)/bin/activate  ## Run security checks
	@echo "Running dependency vulnerability scan..."
	@$(PYTHON) -m safety check || (echo "Security vulnerabilities found in dependencies!" && exit 1)
	@echo "Running static security analysis..."
	@$(PYTHON) -m bandit -r src/ -f custom --msg-template "{relpath}:{line}: {severity}: {msg} ({test_id})" || (echo "Security issues found in code!" && exit 1)
	@echo "Security checks passed!"

test-watch: $(VENV)/bin/activate  ## Run tests in watch mode (requires pytest-watch installed)
	@$(PYTHON) -m pytest_watch --runner "pytest --tb=short -v"

quality: $(VENV)/bin/activate  ## Run all quality checks
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) security
	$(MAKE) test

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: $(VENV)/bin/activate  ## Build package
	$(PYTHON) -m build
