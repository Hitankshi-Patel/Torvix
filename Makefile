# Torvix Makefile for easy development and deployment

.PHONY: help clean install test lint format build publish-test publish-prod all

help:
	@echo "Torvix Development Commands:"
	@echo "  clean        - Clean build artifacts"
	@echo "  install      - Install package in development mode"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  build        - Build package"
	@echo "  publish-test - Publish to TestPyPI"
	@echo "  publish-prod - Publish to PyPI"
	@echo "  all          - Run clean, test, and build"

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true

install:
	@echo "📦 Installing in development mode..."
	pip install -e .[dev]

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=torvix --cov-report=term-missing

lint:
	@echo "🔍 Running linting checks..."
	flake8 torvix tests --max-line-length=88
	mypy torvix

format:
	@echo "✨ Formatting code..."
	black torvix tests
	isort torvix tests

build: clean
	@echo "📦 Building package..."
	pip install build twine
	python -m build
	twine check dist/*

publish-test: build
	@echo "🚀 Publishing to TestPyPI..."
	twine upload --repository testpypi dist/*
	@echo "✅ Published to TestPyPI!"
	@echo "Test with: pip install --index-url https://test.pypi.org/simple/ torvix"

publish-prod: build
	@echo "🚀 Publishing to PyPI..."
	@read -p "Are you sure you want to publish to PyPI? (y/N): " confirm && [ "$$confirm" = "y" ]
	twine upload dist/*
	@echo "✅ Published to PyPI!"

all: clean test build
	@echo "✅ All tasks completed successfully!"

# Development shortcuts
dev-setup:
	@echo "🔧 Setting up development environment..."
	pip install -e .[dev]
	pre-commit install

version:
	@echo "📋 Current version:"
	@grep "__version__" torvix/__init__.py

check-deps:
	@echo "🔍 Checking dependencies..."
	pip-audit
	safety check
