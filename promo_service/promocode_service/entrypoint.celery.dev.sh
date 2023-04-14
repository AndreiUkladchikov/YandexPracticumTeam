#!/bin/sh

load_dev_enviroment () {
  if [ -f /home/promo/web/promocode_service/.env.dev ]
  then
    export $(grep -v '^#' /home/promo/web/promocode_service/.env.dev | xargs)
  else
    echo "File does not exist: /home/promo/web/promocode_service/.env.dev"
    exit 1
  fi
}

load_dev_enviroment

exec "$@"