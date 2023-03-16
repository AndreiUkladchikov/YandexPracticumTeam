import json
from typing import Any

import pika
import requests
from config import settings
from decorators import backoff
from jinja2 import BaseLoader, Environment
from loguru import logger


class MessagePreRender:
    @staticmethod
    def run() -> None:
        """Получаем информацию о сообщении из очереди и обрабатываем."""
        logger.info(
            " [*] Connecting to server {0}:{1} ...".format(
                settings.messages_queue_host, settings.messages_queue_port
            )
        )
        credentials = pika.PlainCredentials(
            settings.messages_queue_username, settings.messages_queue_password
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.messages_queue_host, port=settings.messages_queue_port, credentials=credentials
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=settings.messages_queue, durable=True)
        logger.info(" [*] Waiting for messages from {0} ...".format(settings.messages_queue))
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=settings.messages_queue, on_message_callback=MessagePreRender.process_message
        )
        channel.start_consuming()

    @staticmethod
    def get_user_info(user_id: str) -> dict[str, Any]:
        """Получаем информацию о пользователе по указаному URL."""
        if settings.debug:
            return {"email": "testuser@test.loc", "firstname": "John", "lastname": "Doe"}
        else:
            headers = {"Authorization": "Bearer {0}".format(settings.auth_service_bearer_token)}
            resp = requests.get(url="{0}{1}".format(settings.user_info_url, user_id), headers=headers)
            return resp.json()

    @staticmethod
    def get_film_info(film_id: str) -> dict[str, Any]:
        """Получаем информацию о фильме по указаному URL."""
        if settings.debug:
            return {"title": "Star Wars Episode XXX", "rating": 9.9}
        else:
            resp = requests.get(url="{0}{1}".format(settings.film_info_url, film_id))
            return resp.json()

    @staticmethod
    def render_template(template: str, context: dict[str, Any]) -> str:
        """Рендерим текст сообщения в соответствии с контекстом."""
        rtemplate = Environment(loader=BaseLoader, autoescape=True).from_string(template)
        return rtemplate.render(**context)

    @staticmethod
    def process_message(ch, method, properties, body) -> None:
        """Обрабатываем сообщение в соответствии с контекстом.

        Шаблон входящего сообщения
        message_info: dict[str, Any] = {
            'type': '<service_name>:<message_type>',
            'subject': '<message_topic>',
            'template': '<jinja2_tempate_str>',
            'user_id': '<delivery_user_id>',
            'film_id': '<film_id_optional_for_ugc_service>'
        }
        """
        message_info: dict[
            str,
            Any,
        ] = json.loads(body.decode("utf-8"))
        logger.info(" [o] Received {0}".format(message_info.get("type")))

        render_context = {"user": MessagePreRender.get_user_info(message_info.get("user_id"))}
        if message_info.get("film_id") is not None:
            render_context["film"] = MessagePreRender.get_film_info(message_info.get("film_id"))

        message = {
            "email": render_context.get("user").get("email"),
            "subject": message_info.get("subject"),
            "body": MessagePreRender.render_template(message_info.get("template"), render_context),
        }

        MessagePreRender.send_message(message)
        logger.info(" [o] Message add to {0}".format(settings.send_queue))

    @staticmethod
    @backoff
    def send_message(message: dict[str, Any]) -> int:
        """Добавляет сформирование сообщение в очередь на отправку."""
        credentials = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.send_queue_host,
                    port=settings.send_queue_port,
                    credentials=credentials,
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue=settings.send_queue, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=settings.send_queue,
                body=json.dumps(message).encode("utf-8"),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
        finally:
            connection.close()
