#!/bin/bash
set -e

sh /prestart.sh

# Start Uvicorn with live reload
exec uvicorn --reload --reload-exclude test.log --reload-exclude test.py --host 0.0.0.0 --port 80 --log-level info  src.main:app