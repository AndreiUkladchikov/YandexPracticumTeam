# Запуск проекта

## DEV окружение

Скопируйте и настройте файл ./promocode_service/promocode_service/.env.dev как ./promocode_service/promocode_service/.env

> docker compose -f docker-compose.dev.yaml up -d

## Запуск тестов

Скопируйте и настройте файл ./promocode_service/promocode_service/.env.prod как ./promocode_service/promocode_service/.env

> docker compose -f docker-compose.test.yaml up -d

Результаты

> docker compose logs promoapp

## Prod окружение

Скопируйте и настройте файл ./promocode_service/promocode_service/.env.prod как ./promocode_service/promocode_service/.env

> docker compose -f docker-compose.prod.yaml up -d

Панель аднимитратора будет доступна по ссылке [http://127.0.0.1:8089/admin](http://127.0.0.1:8089/admin)
