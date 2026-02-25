# Makefile commands:
#
# make           - Install dependencies
# make clean     - Delete all builds for a clean slate
# make start     - Launch API Server on local machine
# make stop      - Stop API Server on local machine
# make activate  - Jump into virtualenv environment shell

export PYTHON := $(shell (which python3;which python) 2>/dev/null|head -1|xargs basename)
export PATH := $(shell pwd)/venv/bin:${PATH}
export VIRTUAL_ENV := $(shell pwd)/venv

all: venv/ready.txt Makefile

start: venv/bin/uvicorn
	@make -C api start

stop:
	@make -C api stop

clean:
	rm -rf venv

venv/ready.txt: venv/bin/python venv/bin/wheel requirements.txt Makefile
	true && pip install -r requirements.txt && echo `date` Build Success | tee venv/ready.txt

venv/bin/python:
	$(PYTHON) -m venv venv
	ls -l $@ venv/bin/pip venv/bin/activate
	true && python -V

venv/bin/wheel: venv/bin/python
	$< -m pip install --upgrade pip setuptools wheel
	ls -l $@ && touch $@

venv/bin/uvicorn: venv/ready.txt
	ls -l $@ && touch $@

venv/bin/pip: venv/bin/python
	ls -l $@ && touch $@ && $@ -V

venv/bin/activate: venv/bin/python
	ls -l $@ && touch $@

activate: venv/bin/activate
	@echo 'Type "exit" to leave virtualenv environment'
	@bash -c '. $<; bash'

.PHONY: all clean start stop activate
