import json
import requests
from typing import Any

import pika
from jinja2 import Environment, BaseLoader
from loguru import logger

from common.config import settings
from common.decorators import backoff


class BaseMessageRender:

    def __init__(self) -> None:
        """Получаn информацию о сообщении из очереди."""
        logger.info(
            ' [*] Connecting to server {0}:{1} ...'.format(settings.messages_queue_host,
                                                           settings.messages_queue_port)
        )
        credentials = pika.PlainCredentials(settings.messages_queue_username,
                                            settings.messages_queue_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.messages_queue_host,
                                                                       port=settings.messages_queue_port,
                                                                       credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=settings.messages_queue, durable=True)
        logger.info(' [*] Waiting for messages from {0} ...'.format(settings.messages_queue))
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=settings.messages_queue,
                              on_message_callback=self.process_message)
        channel.start_consuming()

    def get_user_info(self,
                      user_id: str) -> dict[str, Any]:
        """Получаем информацию о пользователе по указаному URL."""
        if settings.debug:
            return {'email': 'testuser@test.loc',
                    'firstname': 'John',
                    'lastname': 'Doe'}
        else:
            headers = {'Authorization': 'Bearer {0}'.format(settings.auth_service_bearer_token)}
            resp = requests.get(url='{0}{1}'.format(settings.user_info_url, user_id), headers=headers)
            return resp.json()

    def get_film_info(self,
                      film_id: str) -> dict[str, Any]:
        """Получаем информацию о фильме по указаному URL."""
        if settings.debug:
            return {'title': 'Star Wars Episode XXX',
                    'rating': 9.9}
        else:
            resp = requests.get(url='{0}{1}'.format(settings.film_info_url, film_id))
            return resp.json()

    def render_template(self, template: str, context: dict[str, Any]) -> str:
        """Рендерим текст сообщения в соответствии с контекстом."""
        rtemplate = Environment(loader=BaseLoader, autoescape=True).from_string(template)
        return rtemplate.render(**context)

    def process_message(self, ch, method, properties, body) -> None:
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
        message_info: dict[str, Any, ] = json.loads(body.decode())
        logger.info(" [o] Received {0}".format(message_info.get('type')))

        render_context = {'user': self.get_user_info(message_info.get('user_id'))}
        if message_info.get('film_id') is not None:
            render_context['film'] = self.get_film_info(message_info.get('film_id'))

        message = {
            'email': render_context.get('user').get('email'),
            'subject': message_info.get('subject'),
            'body': self.render_template(message_info.get('template'), render_context)
        }

        self.send_message(message)
        logger.info(" [o] Message add to {0}".format(settings.send_queue))

    @backoff
    def send_message(self, message: dict[str, Any]) -> int:
        """Добавляет сформирование сообщение в очередь на отправку."""
        credentials = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.send_queue_host,
                                                                       port=settings.send_queue_port,
                                                                       credentials=credentials,))
        channel = connection.channel()
        channel.queue_declare(queue=settings.send_queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=settings.send_queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        connection.close()
