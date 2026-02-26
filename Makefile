# Makefile commands:
#
# make           - Install dependencies
# make start     - Launch API Server
# make stop      - Stop API Server
# make restart   - Restart API server in case recent updates aren't being honored
# make clean     - Delete all builds for a clean slate
# make activate  - Jump into virtualenv environment shell

export PYTHON := $(shell (which python3;echo python) 2>/dev/null|head -1|xargs basename)
export PATH := $(shell pwd)/venv/bin:${PATH}
export VIRTUAL_ENV := $(shell pwd)/venv

all: venv/requirements-setup.txt Makefile api/settings.py

clean:
	make stop || true
	rm -rf venv

start: venv/bin/uvicorn
	@make -C api start

stop:
	@make -C api stop

restart:
	@make -C api restart

api/settings.py:
	@make -C api settings.py

venv/requirements-setup.txt: venv/bin/wheel requirements.txt Makefile
	true && pip install -r requirements.txt && echo `date` Build Success | tee $@

venv/bin/python venv/bin/pip venv/bin/activate: venv/virtualenv-setup.txt

venv/virtualenv-setup.txt: Makefile
	true && $(PYTHON) -m venv venv
	@ls -l venv/bin/python venv/bin/pip venv/bin/activate && touch -c -h venv/bin/python venv/bin/pip venv/bin/activate
	true && python -V
	@echo `date` venv is ready | tee $@

venv/bin/wheel: venv/bin/python
	true && python -m pip install --upgrade pip setuptools wheel
	@ls -l $@ && touch -c -h $@

venv/bin/uvicorn: venv/requirements-setup.txt
	@ls -l $@ && touch -c -h $@ # Santity check just to ensure uvicorn was actually installed

activate: venv/bin/activate
	@echo 'Type "exit" to leave virtualenv environment'
	@bash -c '. $<; exec bash'

.PHONY: start stop restart clean activate
