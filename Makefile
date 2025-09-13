# Makefile for debug-cli project

.PHONY: help install install-dev test lint format clean build docker-build docker-run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	pytest tests/ -v --cov=debug_cli --cov-report=term-missing

lint: ## Run linting
	flake8 debug_cli/ tests/
	mypy debug_cli/

format: ## Format code
	black debug_cli/ tests/
	isort debug_cli/ tests/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	python -m build




setup-env: ## Set up environment file
	cp .env.example .env
	@echo "Please edit .env file with your OpenAI API key"

check-env: ## Check environment setup
	@echo "Checking environment..."
	@python -c "import os; print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
	@python -c "import os; print('SHELL:', os.getenv('SHELL', 'NOT SET'))"

all: clean install-dev test lint format build ## Run all checks and build

# GitHub Actions related commands
ci-test: ## Run the same tests as GitHub Actions
	pytest tests/ -v --cov=debug_cli --cov-report=term-missing

ci-lint: ## Run the same linting as GitHub Actions
	flake8 debug_cli/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 debug_cli/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

ci-format: ## Run the same formatting checks as GitHub Actions
	black --check debug_cli/ tests/
	isort --check-only debug_cli/ tests/

ci-typecheck: ## Run the same type checking as GitHub Actions
	mypy debug_cli/ --ignore-missing-imports

ci-security: ## Run the same security checks as GitHub Actions
	safety check
	bandit -r debug_cli/

ci-all: ci-lint ci-format ci-typecheck ci-test ci-security ## Run all CI checks locally

# Docker commands
docker-build: ## Build Docker image
	docker build -t debug-cli:latest .

docker-run: ## Run Docker container with help
	docker run --rm debug-cli:latest

docker-run-interactive: ## Run Docker container interactively
	docker run --rm -it debug-cli:latest bash

docker-test: ## Test Docker container functionality
	docker run --rm -e OPENAI_API_KEY=$${OPENAI_API_KEY} debug-cli:latest config

docker-compose-up: ## Start services with docker-compose
	docker-compose up --build

docker-compose-dev: ## Start development environment
	docker-compose --profile dev up --build debug-cli-dev

docker-compose-down: ## Stop and remove containers
	docker-compose down

docker-clean: ## Clean up Docker resources
	docker system prune -f
	docker image prune -f

docker-all: docker-build docker-test ## Build and test Docker image

