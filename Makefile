.PHONY: help install install-dev test coverage lint format build clean publish-test publish

help:
	@echo "Available targets:"
	@echo "  install      - Install package in editable mode"
	@echo "  install-dev  - Install package with dev dependencies"
	@echo "  test         - Run tests with pytest"
	@echo "  coverage     - Run tests with coverage report"
	@echo "  lint         - Run code quality checks"
	@echo "  format       - Format code with black and isort"
	@echo "  build        - Build distribution packages"
	@echo "  clean        - Remove build artifacts"
	@echo "  publish-test - Publish to TestPyPI"
	@echo "  publish      - Publish to PyPI"

install:
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v

coverage:
	pytest --cov=airflow_config --cov-report=html --cov-report=term-missing

lint:
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

build: clean
	python3 -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

publish-test: build
	twine upload --repository testpypi dist/*

publish: build
	twine upload dist/*
