#!/bin/sh

gunicorn movies.wsgi:application --bind 0.0.0.0:8080

exec "$@"