### Сервис нотификации

Схема сервиса добавлена в schemas (PlantUML - файл) - Architecture_TO_BE.puml

Сервис нотификации, функциональность:
- AdminPanel - заполнение шаблонов, создание рассылок
- API - получение сообщений из сторонних сервисов и постановка в очередь
- Очередь - RabbitMQ
- ETL - обработка сообщений из очереди и постановка в очередь на отправку
- Sender worker - отправка сообщений через SMTP сервис

AdminPanel:
В качестве фреймворка выбрали Django

API:
Django Rest Framework.
Выбрали так как одна из ручек API должна отдавать шаблоны, удобно собрать все в одном сервисе

RabbitMQ:
Очередь auth_messages - "сырые" письма. 
Очередь send_auth_messages - отрендеренные по шаблону и готовые к отправке

Как запустить:
- docker-compose build
- docker-compose -f docker-compose.yml up -d