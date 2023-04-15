# Запуск проекта

## DEV окружение

Установите зависимости из promocode_service/requirements.txt и promocode_service/requirements.dev.txt

> pipenv install -r promocode_service/requirements.txt && pipenv install -r promocode_service/requirements.dev.txt

Скопируйте и настройте файл ./promocode_service/promocode_service/.env.dev как ./promocode_service/promocode_service/.env

Запустите сервер PostgreSQL и Redis. Запустите Celery и Celery Beat.

> celery -A promocode_service worker -l info

> celery -A promocode_service beat -l info

При необходимости запустите Flower

> celery flower -A promocode_service --port=5555 --broker=redis://127.0.0.1:6379/0

Запустите Django

> python manage.py runserver 0.0.0.0:8000

## DEV окружение в Docker

Скопируйте и настройте файл ./promocode_service/promocode_service/.env.dev как ./promocode_service/promocode_service/.env

> docker compose -f docker-compose.dev.yaml up -d

## Запуск тестов

Скопируйте и настройте файл ./promocode_service/promocode_service/.env.dev как ./promocode_service/promocode_service/.env

> docker compose -f docker-compose.test.yaml up -d

Результаты

> docker compose logs promoapp

## Prod окружение

Скопируйте и настройте файл ./promocode_service/promocode_service/.env.prod как ./promocode_service/promocode_service/.env

> docker compose -f docker-compose.yaml up -d

Панель аднимитратора будет доступна по ссылке [http://127.0.0.1:8089/promoadmin](http://127.0.0.1:8089/promoadmin)

Документация по API сервиса доступна по ссылке [http://127.0.0.1:8089/api/v1/schema/swagger-ui/](http://127.0.0.1:8089/api/v1/schema/swagger-ui/)

* Логин и пароль администратора указывается в .env и будет создан при запуске контейнера.
