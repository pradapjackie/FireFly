#!/bin/bash
set -e

sh /prestart.sh

exec gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py src.main:app
