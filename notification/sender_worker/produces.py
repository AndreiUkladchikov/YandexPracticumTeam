import json

import pika
import pika.exceptions
from loguru import logger

from common.config import settings


def rabbit_producer(queue: str, template: dict[str, str]):
    """
    Функция для тестовой отправки писем (mail, change_password) в очередь
    :param queue: название очереди
    :param template: сообщение
    :return:
    """
    cred = pika.PlainCredentials(
        settings.send_queue_username, settings.send_queue_password
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.send_queue_host, credentials=cred)
    )
    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue)

        channel.basic_publish(
            exchange="",
            routing_key=settings.send_queue,
            body=json.dumps(template).encode(),
        )
    except pika.exceptions as e:
        logger.exception(e)
    finally:
        connection.close()
