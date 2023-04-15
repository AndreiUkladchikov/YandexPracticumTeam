#!/bin/sh

load_prod_enviroment () {
  if [ -f /home/promo/web/promocode_service/.env.prod ]
  then
    export $(grep -v '^#' /home/promo/web/promocode_service/.env.prod | xargs)
  else
    echo "File does not exist: /home/promo/web/promocode_service/.env.prod"
    exit 1
  fi
}

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

load_prod_enviroment
check_postgres_db
start_prod_server

gunicorn promocode_service.wsgi:application --bind 0.0.0.0:8000

exec "$@"