# YandexPracticumTeam
- db_create - заполнение для postgres
- postgres_to_es - etl сервис
- fast_api - задание спринта


Все нужные сервисы собраны в одном проекте (один docker-compose):
- Postgres
- ETL
- Fast API
- Elasticsearch
- Redis

Как запустить:
- docker-compose build
- docker-compose -f docker-compose.yml up -d

Запустить в виртуальном окружение (requirements.txt внутри папки):
- Создать базу: python db_create/create_pgdb.py
- Заполнить базу данными из sqlite: python db_create/main.py
- перезапустить ETL container
