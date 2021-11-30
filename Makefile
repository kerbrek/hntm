.DEFAULT_GOAL := help

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

## https://stackoverflow.com/a/45843594/6475258
.PHONY: help # Print list of targets with descriptions
help:
	@grep '^.PHONY: .* #' $(lastword $(MAKEFILE_LIST)) | sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' | expand -t20

## https://stackoverflow.com/a/26339924/6475258
# .PHONY: list # Print list of targets
# list:
# 	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
