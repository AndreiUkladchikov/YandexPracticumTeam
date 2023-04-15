#!/bin/sh

celery -A promocode_service beat -l info

exec "$@"