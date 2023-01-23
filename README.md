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
docker-compose-auth - сервис авторизации (Flask + Postgre + Redis)

Документация по Flask API (мы используем spectree):
http://localhost:5001/apidoc/swagger/
http://localhost:5001/apidoc/redoc/
