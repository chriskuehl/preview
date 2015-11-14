BIN := virtualenv_run/bin
PYTHON := $(BIN)/python
export PYTHONPATH = $(PWD)

.PHONY: test
test: virtualenv_run
	$(BIN)/py.test tests/
	$(BIN)/pre-commit run --all-files

.PHONY: test-dev
test-dev: virtualenv_run
	$(BIN)/py.test -s -v --pdb tests/

.PHONY: dev
dev: virtualenv_run
	$(PYTHON) -m preview.webapp.run --debug

.PHONY: worker-dev
worker-dev: virtualenv_run
	$(PYTHON) -m preview.worker.run --debug

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
		pip freeze | grep -vE '^(preview==|\-e)' > requirements.txt || true

virtualenv_run: requirements.txt requirements-dev.txt
	./vendor/venv-update -ppython3 virtualenv_run requirements.txt requirements-dev.txt
