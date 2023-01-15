#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
  echo $DB_HOST
done
echo "PostgreSQL started"

gunicorn movies.wsgi:application --bind 0.0.0.0:8080

exec "$@"