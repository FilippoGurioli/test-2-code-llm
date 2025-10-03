# Makefile for T2C development

.PHONY: help install install-dev test test-unit test-integration lint format type-check clean build docs

# Default Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	$(PIP) install -e .

install-dev:  ## Install package with development dependencies
	$(PIP) install -e ".[dev]"
	pre-commit install

test:  ## Run all tests
	pytest

test-coverage:  ## Run tests with coverage report
	pytest --cov=src/t2c --cov-report=html --cov-report=term-missing

lint:  ## Run linting (ruff)
	ruff check src/ tests/

format:  ## Format code (black + ruff)
	black src/ tests/
	ruff check --fix src/ tests/

type-check:  ## Run type checking (mypy)
	mypy src/t2c/

quality:  ## Run all quality checks
	$(MAKE) lint
	$(MAKE) type-check
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

build:  ## Build package
	$(PYTHON) -m build
