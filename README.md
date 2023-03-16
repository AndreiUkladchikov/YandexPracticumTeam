[![Build Status](https://github.com/AndreiUkladchikov/YandexPracticumTeam/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/AndreiUkladchikov/YandexPracticumTeam/actions/workflows/checks.yml)
# YandexPracticumTeam
Схема сервисов:
- schemas
- в виде картинок - out/schemas


For Production:
- prod_env/docker-compose-prod
- prod_env/docker-compose-auth

For Develop (in root folder):
- docker-compose
- docker-compose-auth

For Run with Tests:
- Советуем запускать в отдельном compose, т.к. часть тестов - это очистка эластика и проверка кэша
- docker-compose-with-tests

Как запустить:
- docker-compose build
- docker-compose -f docker-compose.yml up -d

Запустить в виртуальном окружении (requirements.txt внутри папки):
- Создать базу: python db_create/create_pgdb.py
- Заполнить базу данными из sqlite: python db_create/main.py
- создать схемы в Elastic - postgres_to_es/create_etl.py
- перезапустить ETL container

Документация по Fast Api:
http://localhost:8080/api/openapi

# Спринт 6
docker-compose-auth - сервис авторизации (Flask + Postgres + Redis)

Документация по Flask API (мы используем spectree):
http://localhost:5001/apidoc/swagger/
http://localhost:5001/apidoc/redoc/

# Спринт 7
В качестве сервиса для авторизации через OAuth2 был выбран Яндекс (https://yandex.ru/dev/id/doc/dg/api-id/concepts/adoption.html)

- После регистрации своего приложения был получен CliendID, Client Secret, а также назначен Redirect URl (На этот адрес будет перенаправлен пользователь после авторизации)

- Для авторизации на FilmService необходимо в браузере перейти на эндпоинт /oauth-login (v1/auth/oauth.py), далее пользователь будет перенаправлен в Яндекс.OAuth, где ему нужно будет дать разрешение на предоставление данных в FilmService

- Далее Яндекс.OAuth выдает временный код (code) и перенаправляет пользователя на Redirect URl (code в параметрах запроса)

- В качестве Redirect URl задан тот же эндпоинт /oauth-login, но в случаи, если задан code, тогда идет запрос на Яндекс.OAuth для получения токенов доступа

- С помощью access_token у Яндекс.OAuth мы будем иметь доступ к данным пользователя

Для запуска воспользуемся командой: docker-compose -f docker-compose-auth.yml --env-file=flask_app/.env up -d 

После запуска контейнеров необходимо:

1) осуществить миграции:  docker exec -it auth_server alembic upgrade head
2) сгенерировать основные роли: docker exec -it auth_server python create_roles.py


# Спринт 8
Для старта сервисов: docker-compose -f docker-compose-ugc.yaml --env-file .ugc.env --build up -d 

Основные моменты в ETL:
- в Clickhouse пишем по 10.000 записей
- данные из Kafka храним в Redis до достижения 10.000 записей

Docker Compose файл для продакшн среды находится в ./prod_env

# Спринт 9
Было решено объединить backend сервис из прошлого спринта и сервис ugc_backend (ugc_backend/)

Для старта сервисов: docker-compose -f docker-compose-ugc.yaml --env-file .ugc.env --build up -d

Сравнение производительности [mongo и postgres](https://github.com/AndreiUkladchikov/YandexPracticumTeam/tree/main/load_tests)

В проект было добавлено логгирование (docker-compose-elk.yml) для сервиса ugc_backend и nginx

# Спринт 10
Сервис нотификации, функциональность:
- AdminPanel - заполнение шаблонов, создание рассылок
- API - получение сообщений из сторонних сервисов и постановка в очередь
- Очередь - RabbitMQ
- ETL - обработка сообщений из очереди и постановка в очередь на отправку
- Sender worker - отправка сообщений через SMTP сервис

Папка notification:
- rabbitmq - очередь сообщений
- etl - обработка сообщений. Получаем из очереди, рендерим (по шаблону из django) и отправка в sender
- sender - обработка отрендеренных сообщений из очереди через smtp клиент (использовали MailHog)
- django - админка (создание шаблонов для рендера + можно будет использовать для создания массовых рассылок) и DRF - API для отправки сообщений в очередь и для получения шаблонов

# Team
- Андрей Укладчиков
- Андрей Гладченко
- Михаил Ботусов
- Ростислав Сулицкий
