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

## Шаблон  исходящего сообщения

message = {
    'email': <email_where_message_must_be_send>,
    'subject': <email_subject>,
    'body': <email_text_body>
}
