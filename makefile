VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(VENV)/bin/python -m pip
pip-tools=$(VENV)/bin/python -m piptools

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'


.PHONY: clean venv update develop install

install: venv update

clean:
	@echo -e $(bold)Clean up virtualenv and cache directories$(sgr0)
	@rm -rf $(VENV) *.egg-info .pytest_cache

venv: clean
	@echo -e $(bold)Create a new virtualenv$(sgr0)
	@python3 -m venv $(VENV)
	@$(pip) install --upgrade pip pip-tools

update:
	@echo -e $(bold)Install and update requirements$(sgr0)
	@$(pip-tools) sync 

develop: update
	@echo -e $(bold)Install and update development requirements$(sgr0)
	$(pip) install black isort pytest


.PHONY: requirements

requirements:
	@echo -e $(bold)Update requirements with pip-tools$(sgr0)
	$(VENV)/bin/pip-compile -vU \
		--resolver backtracking \
		--output-file requirements.txt \
		requirements.in

.PHONY: test
test:
	@$(python) -m pytest

