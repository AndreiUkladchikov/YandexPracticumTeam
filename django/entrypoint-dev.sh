#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
  echo $DB_HOST
done
echo "PostgreSQL started"

python db_create/create_pgdb.py

python manage.py migrate

DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput

python db_create/main.py

gunicorn movies.wsgi:application --bind 0.0.0.0:8080

exec "$@"