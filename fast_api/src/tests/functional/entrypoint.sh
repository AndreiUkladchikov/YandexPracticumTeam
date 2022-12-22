#!/bin/sh

python /functional/utils/wait_for_es.py

python /functional/utils/wait_for_redis.py

pytest

exec "$@"