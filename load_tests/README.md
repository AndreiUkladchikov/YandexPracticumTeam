# Тестирование MongoDB

## Запуск шарда MongoDB
- Скопируйте .env.example как .env
- Запустите MongoDB docker compose up -d
- Сконфигурируйте шард, создайте тестовую БД и коллекции, запустив скрипт configure.sh

## Запуск тестов
- создайте виртуальное окружение python, например: pipenv install -r tester/requirements.txt && pipenv shell
- запустите тесты: python tester/main.py


## Запуск Postgres
load_tests/postgres :
- python create_db.py (создаем таблицу)
- python create_data.py (наполняем фейковыми данными)
- запуск тестов python tests.py

Результат:
Write 1 row in 24.266 ms
Read 1 row in 13.216 ms
Write 1 row in 13.942 ms
Read 1 row in 12.164 ms
Write 1 row in 28.636 ms
Read 1 row in 12.317 ms
Write 1 row in 13.044 ms
Read 1 row in 34.002 ms..

## Выводы
- Оба хранилища показали быструю скорость чтения
- MongoDB поддерживает JSON query, что может очень пригодится при дальнейшнем развитии сервиса
- MongoDB - возможность реплицирования на разных серверах

Выбираем MongoDB в качестве хранилща
