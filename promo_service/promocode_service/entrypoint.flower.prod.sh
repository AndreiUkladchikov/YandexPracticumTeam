#!/bin/sh

celery flower -A promocode_service --port=5555 --broker=redis://redis:6379/0

exec "$@"