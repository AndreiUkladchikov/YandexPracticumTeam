# Обработчик сообщений из notification service

Получаn информацию о сообщении из очереди. Обрабатываем сообщение в соответствии с контекстом. Получает необходимую информацию о пользователе и фильме при необходимости. Рендит персонализированное письмо. Добавляет сформирование сообщение в очередь на отправку.

## Шаблон входящего сообщения

message_info: dict[str, Any] = {
    'type': '<service_name>:<message_type>',
    'subject': '<message_topic>',
    'template': '<jinja2_tempate_str>',
    'user_id': '<delivery_user_id>',
    'film_id': '<film_id_optional_for_ugc_service>'
}

* film_id параметр передается опционально, при наличии worker обратится к film async api за данными фильма по указанному в окружении URL.

## Контекст для отрисовки шаблона передается в следующей форме

context: dict[str, Any] = {
    'user': {
        'email': 'test@test.loc',
        'firstname': 'John',
        ...
    },
    'film': {
        'title': 'Star Wars',
        'raiting': 9.9,
        ...
    },
}

## Пример шаблона сообщения

template = '{{ user.get('firstname', 'Товарищ') }}, ваш отзыв к фильму {{ film.get('title', '') }} понравился пользователю!'

Обращаться к нужным полям можно с помощью метода get для dict и при необходимости указать значения по умолчанию, если auth api или film async api вернет некорректный ответ.

## Шаблон  исходящего сообщения

message = {
    'email': <email_where_message_must_be_send>,
    'subject': <email_subject>,
    'body': <email_text_body>
}

## Запуск функциональных тестов в контейнере (не забудьте настроить тестовое окружение, пример .env.test.example)

docker exec -it etl3 python -m pytest

## Или в окружении

pipenv install -r notification/etl_worker/requirements.txt
cd notification/etl_worker
python -m pytest

## Выбор синхронной модели

Выбрали синхронную модель, так как воркер относительно универсальный и масштабировать планировали горизонтально в дальнейшем разделяя сообщения на тематические очереди и подымая нужное количество реплик воркера под очередь. В целом в перспективе с ростом нагрузки да необходимо будет перейти на ассинхронную модель.
