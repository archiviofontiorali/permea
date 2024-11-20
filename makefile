VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
uv?=uv

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'

.PHONY: init
init: venv update

.PHONY: clean
clean:
	@echo -e $(bold)Clean up old virtualenv and cache$(sgr0)
	rm -rf $(VENV) *.egg-info

.PHONY: venv
venv: clean
	@echo -e $(bold)Create virtualenv$(sgr0)
	@$(uv) venv --python 3.12 $(VENV)

.PHONY: update
update:
	@echo -e $(bold)Install and update requirements$(sgr0)
	$(uv) pip sync requirements.dev.txt
	$(uv) pip install --editable .

.PHONY: requirements
requirements: 
	$(uv) pip compile --universal --upgrade \
			--output-file requirements.txt pyproject.toml
	$(uv) pip compile --universal --upgrade --extra dev \
			--output-file requirements.dev.txt pyproject.toml


.PHONY: test
test:
	$(python) -m pytest -x -p no:warnings
