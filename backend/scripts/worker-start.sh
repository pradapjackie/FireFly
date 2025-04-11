#!/bin/bash
set -e

celery -A src.core.celery_app worker --concurrency=10 --loglevel=INFO -Q main-queue -n $WORKER_NAME@%h
