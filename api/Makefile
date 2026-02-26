# Makefile commands:
#
# make           - Make sure dependencies are ready
# make start     - Launch API Server
# make stop      - Stop API Server
# make restart   - Restart API server in case recent updates aren't being honored

all: ../venv/requirements-setup.txt settings.py

start: ../venv/requirements-setup.txt settings.py
	@[ ! -f api.pid ] || ! kill -0 `cat api.pid` 2>/dev/null || (echo Process `cat api.pid` already running. && exit 1)
	(uvicorn api:app --reload & echo $$! > api.pid) >> console.log 2>> console.err

stop:
	@(kill -0 `cat api.pid 2>/dev/null` 2>/dev/null && echo Stopping uvicorn ... && kill -INT `cat api.pid`) || echo No uvicorn process found.

restart: ../venv/requirements-setup.txt settings.py
	@make stop && sleep 2 && make start

../venv/requirements-setup.txt:
	@sleep 1 && echo Building dependencies ...
	make -C .. venv/requirements-setup.txt

settings.py:
	@echo 'Missing settings.py!'
	@echo HINT: cp -vin `pwd`/settings.py.example `pwd`/settings.py
	@exit 1

.PHONY: all start stop restart
