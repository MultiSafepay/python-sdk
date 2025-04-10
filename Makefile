POETRY ?= poetry run
MIN_TEST_COVERAGE ?= 70

#####################
# Build commands #
#####################

check-prereqs:
	@echo "=> Checking for pre-requisites"
	@if ! poetry --version; then echo "=> Poetry isn't installed" && exit 1; fi
	@echo "=> All pre-requisites satisfied"

venv: check-prereqs
	@echo "=> Use the venv"
	poetry env use .venv/bin/python

install: check-prereqs venv
	@echo "=> Installing python dependencies"
	poetry install

##########################
# Formatting and linting #
##########################

format: ## runs code formatting
	@echo "=> Running code formatting"
	@echo "============================="
	$(POETRY) black src tests
	$(POETRY) ruff check --fix src tests
	@echo "============================="
	@echo "=> Code formatting complete"

format-check: ## runs code formatting checks
	@echo "=> Running code formatting checks"
	@echo "============================="
	$(POETRY) black --check src tests
	$(POETRY) ruff check --exit-non-zero-on-fix src tests
	@echo "============================="
	@echo "=> All formatting checks succeeded"

static-type-check: ## runs static type check
	@echo "============================="
	@echo "=> Running static type checker"
	@echo "============================="
	$(POETRY) mypy src
	@echo "============================="
	@echo "=> Static type check succeeded"

lint: format-check
	@echo "============================="
	@echo "=> Running linter"
	@echo "============================="
	$(POETRY) pylint src tests
	@echo "============================="
	@echo "=> Linter succeeded"

#################
# Test commands #
#################

test:
	@echo "=> Running unit tests"
	@echo "===================================="
	$(POETRY) pytest --cov=src --reruns=1 -k "not e2e"

test-e2e:
	@echo "=> Running e2e tests"
	@echo "===================================="
	$(POETRY) pytest tests/multisafepay/e2e/ --reruns=1

test-audit: test
	@echo "=> Running test coverage report"
	@echo "===================================="
	$(POETRY) coverage report --show-missing --fail-under=$(MIN_TEST_COVERAGE)

test-report: test
	@echo "=> Running test coverage report"
	@echo "===================================="
	$(POETRY) coverage xml
