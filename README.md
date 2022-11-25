# YandexPracticumTeam
- db_create - заполнение для postgres
- postgres_to_es - etl сервис
- fast_api - задание спринта


Все нужные сервисы собраны в одном проекте (один docker-compose):
- Postgres
- ETL
- Fast API
- Elasticsearch

После запуска контейнеров:
- Создать базу: python db_create/create_pgdb.py
- Заполнить базу данными из sqlite: python db_create/main.py
- создать схемы для ETL: python postgres_to_es/create_etl.py
