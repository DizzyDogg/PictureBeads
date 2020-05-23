Server Tech
###########

Web server for static and frontend:
nginx or LigHTTPd? nginx

Web server for API:
uvicorn or hypercorn or daphne? Uvicorn for now, but we can switch to Hypercorn in the future if we need one or more features it provides enough to justify the slightly slower speed

Async web framework for the API:
FastAPI or Quart? FastAPI


Running Services
################

Installing Python Packages
==========================

In a Python3 virtualenv, run:

 pip install -r requirements.txt

API
===

In the api/ directory, while in the virtualenv, run:

 uvicorn api:app --reload

Website
=======

In this directory:

 nginx -p . -c nginx.conf -g "daemon off;"
