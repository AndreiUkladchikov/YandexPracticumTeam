# YandexPracticumTeam
docker-compose-dev (или prod) - апи для фильмов:
- FastApi
- Postgre
- Elastic
- Redis
- ETL
- Tests

Как запустить:
- docker-compose build
- docker-compose -f docker-compose.yml up -d

Запустить в виртуальном окружении (requirements.txt внутри папки):
- Создать базу: python db_create/create_pgdb.py
- Заполнить базу данными из sqlite: python db_create/main.py
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

- После регистрации своего приложения был получен CliendID, Client Secret, а также назначен Redirect URl (На этот адрес будет пользователь после авторизации)

- Для авторизации на FilmService необходимо в браузере перейти на эндпоинт /oauth-login (v1/auth/oauth.py), далее пользователь будет перенаправлен в Яндекс.OAuth, где ему нужно будет дать разрешение на предоставление данных в FilmService

- Далее Яндекс.OAuth выдает временный код (code) и перенаправляет пользователя на Redirect URl (code в параметрах запроса)

- В качестве Redirect URl задан тот же эндпоинт /oauth-login, но в случаи, если задан code, тогда идет запрос на Яндекс.OAuth для получения токенов доступа

- С помощью access_token у Яндекс.OAuth мы будем иметь доступ к данным пользователя






