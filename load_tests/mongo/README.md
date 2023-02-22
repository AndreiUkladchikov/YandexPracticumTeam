# Тестирование MongoDB

## Запуск шарда MongoDB
- Скопируйте .env.example как .env
- Запустите MongoDB docker compose up -d
- Сконфигурируйте шард, создайте тестовую БД и коллекции, запустив скрипт configure.sh

## Запуск тестов
- создайте виртуальное окружение python, например: pipenv install -r tester/requirements.txt && pipenv shell
- запустите тесты: python tester/main.py
