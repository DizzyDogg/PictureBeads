# Makefile commands:
#
# make           - Install dependencies
# make clean     - Delete all builds for a clean slate
# make start     - Launch API Server on local machine
# make stop      - Stop API Server on local machine
# make activate  - Jump into virtualenv environment shell

export PATH := $(shell pwd)/venv/bin:${PATH}
export VIRTUAL_ENV := $(shell pwd)/venv

all: venv/ready.txt Makefile

start: venv/bin/uvicorn
	@make -C api start

stop:
	@(kill -0 `cat api/api.pid 2>/dev/null` 2>/dev/null && echo Stopping uvicorn ... && kill -INT `cat api/api.pid`) || echo No uvicorn process found.

clean:
	rm -rf venv

venv/ready.txt: venv/bin/python venv/bin/pip venv/bin/activate requirements.txt Makefile
	pip install --upgrade pip
	pip install -r requirements.txt && echo `date` Build Success | tee venv/ready.txt

venv/bin/uvicorn: venv/ready.txt

venv/bin/pip: venv/bin/python venv/bin/activate
	[ ! -L venv/bin/pip -a -x venv/bin/pip ] && touch -h venv/bin/pip || true
	[ -x venv/bin/pip ] || (which pip && cp -v -p `which pip` venv/bin/pip) || (which pip3 && cp -v -p `which pip3` venv/bin/pip) || true
	[ -x venv/bin/pip ] && ls -l venv/bin/pip && echo venv/bin/pip is installed. && pip -V

venv/bin/python:
	mkdir -v -p venv/bin
	[ -x venv/bin/python ] || rm -f -v venv/bin/python
	(which python && ln -s -v -f `which python` venv/bin/python) || (which python3 && ln -s -v -f `which python3` venv/bin/python)
	[ -x venv/bin/python ] && ls -l venv/bin/python && echo venv/bin/python is installed. && python -V

venv/bin/activate: venv/bin/python
	python -m venv venv

activate:
	@echo 'Type "exit" to leave virtualenv environment'
	@bash -c '. venv/bin/activate; bash -i'

.PHONY: all clean test start stop activate
