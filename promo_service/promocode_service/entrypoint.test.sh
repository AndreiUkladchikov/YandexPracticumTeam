#!/bin/sh

check_postgres_db () {
	echo "Waiting for postgres..."

	while ! nc -z $DB_HOST $DB_PORT; do
		sleep 0.1
	done

	echo "PostgreSQL started"
}

start_prod_server () {
  echo "Starting production enviroment..."

  python manage.py migrate --noinput
  echo "Migrations complete!"

  python manage.py collectstatic --no-input --clear
  echo "Collect static complete!"

	python manage.py compilemessages
  echo "Update translations complete!"

  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJ_USERNAME', '$DJ_USER_EMAIL', '$DJ_PASSWORD');" | python manage.py shell
}

check_postgres_db
start_prod_server

python manage.py test promocode.tests

exec "$@"