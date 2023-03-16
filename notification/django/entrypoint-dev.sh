#!/bin/sh

python manage.py migrate

DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput

gunicorn movies.wsgi:application --bind 0.0.0.0:8080

exec "$@"