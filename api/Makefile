# Makefile commands:
#
# make start     - Launch API Server on local machine
# make stop      - Stop API Server on local machine

all: ../venv/ready.txt

start: ../venv/ready.txt settings.py
	@[ ! -f api.pid ] || ! kill -0 `cat api.pid` 2>/dev/null || (echo Process `cat api.pid` already running. && exit 1)
	uvicorn api:app --reload & echo $$! > api.pid

stop:
	@(kill -0 `cat api.pid 2>/dev/null` 2>/dev/null && echo Stopping uvicorn ... && kill -INT `cat api.pid`) || echo No uvicorn process found.

../venv/ready.txt:
	sleep 1 && echo Building dependencies ...
	make -C .. venv/ready.txt

.PHONY: all start stop
