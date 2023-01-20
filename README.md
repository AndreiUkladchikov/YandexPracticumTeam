# YandexPracticumTeam
- db_create - заполнение для postgres
- postgres_to_es - etl сервис
- fast_api - задание спринта


Настройки для compose: docker-settings-sample.env


Все нужные сервисы собраны в одном проекте (один docker-compose):
- Postgres
- ETL
- Fast API
- Elasticsearch
- Redis

Как запустить:
- docker-compose build
- docker-compose -f docker-compose.yml up -d

Запустить в виртуальном окружении (requirements.txt внутри папки):
- Создать базу: python db_create/create_pgdb.py
- Заполнить базу данными из sqlite: python db_create/main.py
- перезапустить ETL container

# Спринт 6
docker-compose-auth - сервис авторизации (Flask + Postgre + Redis)
docker-compose-dev (или prod) - апи для фильмов

Настройка:
Если есть старые контейнеры - удалить postgres и elastic и поднять их заново
- db_create/create_pgdb.py - добавлена колонка access_level в Postgres
- db_create/main.py - рандомно выставляет уровень доступа к фильмам (это же тестовые данные) - например только для пользователей с подпиской
- postgres_to_es/create_etl.py - создать новые схемы (предварительно удалить movies - curl -X DELETE 'http://localhost:9200/movies')
