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

celery -A promocode_service beat -l info

exec "$@"