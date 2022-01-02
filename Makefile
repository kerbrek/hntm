.DEFAULT_GOAL := help

SHELL := /usr/bin/env bash

.PHONY: setup # Setup a working environment
setup:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

.PHONY: shell # Spawn a shell within the virtual environment
shell:
	pipenv shell

.PHONY: lint # Run linter
lint:
	pipenv run pylint hntm/

.PHONY: test # Run tests
test:
	pipenv run pytest tests/

.PHONY: coverage # Run tests with coverage report
coverage:
	pipenv run pytest --cov-report term-missing:skip-covered --cov=hntm tests/

.PHONY: start # Start application server
start:
	pipenv run python -m hntm.proxy

.PHONY: requirements # Generate requirements.txt file
requirements:
	pipenv lock --requirements > requirements.txt

.PHONY: help # Print list of targets with descriptions
help:
	@echo; \
		for mk in $(MAKEFILE_LIST); do \
			echo \# $$mk; \
			grep '^.PHONY: .* #' $$mk | sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' | expand -t20; \
			echo; \
		done
