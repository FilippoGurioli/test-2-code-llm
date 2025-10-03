# Makefile for T2C development

.PHONY: help install install-dev test test-coverage test-watch lint format type-check security quality clean build

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
	pre-commit install --hook-type commit-msg

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

security:  ## Run security checks
	@echo "🔍 Running dependency vulnerability scan..."
	@safety check || (echo "❌ Security vulnerabilities found in dependencies!" && exit 1)
	@echo "🔒 Running static security analysis..."
	@bandit -r src/ -f custom --msg-template "{relpath}:{line}: {severity}: {msg} ({test_id})" || (echo "❌ Security issues found in code!" && exit 1)
	@echo "✅ Security checks passed!"

test-watch:  ## Run tests in watch mode
	pytest-watch --runner "pytest --tb=short -v"

quality:  ## Run all quality checks
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

build:  ## Build package
	$(PYTHON) -m build
