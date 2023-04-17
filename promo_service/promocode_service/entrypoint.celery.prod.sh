#!/bin/sh

celery -A promocode_service worker -l info

exec "$@"