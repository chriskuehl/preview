BIN := virtualenv_run/bin
PYTHON := $(BIN)/python
export PYTHONPATH = $(PWD)

.PHONY: test
test: virtualenv_run
	$(BIN)/pre-commit run --all-files

.PHONY: dev
dev: virtualenv_run
	$(PYTHON) -m preview.app

.PHONY: install-hooks
install-hooks: virtualenv_run
	$(BIN)/pre-commit install -f --install-hooks

.PHONY: update-requirements
update-requirements:
	$(eval TMP := $(shell mktemp -d))
	virtualenv -p python3 $(TMP)
	. $(TMP)/bin/activate && \
		pip install --upgrade pip && \
		pip install . && \
		pip freeze | grep -v '^preview==' > requirements.txt || true

virtualenv_run: requirements.txt requirements-dev.txt
	python ./vendor/venv-update -ppython3 virtualenv_run requirements.txt requirements-dev.txt