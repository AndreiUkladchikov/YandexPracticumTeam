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

load_prod_enviroment

celery flower -A promocode_service --port=5555 --broker=redis://redis:6379/0

exec "$@"