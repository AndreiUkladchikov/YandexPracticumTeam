from http import HTTPStatus

import pika
from pika import exceptions

from admin_panel.config import settings
from admin_panel.models import MessageModel


def send_message(message: MessageModel):
    cred = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.send_queue_host, credentials=cred))
    try:
        channel = connection.channel()
        channel.queue_declare(queue=settings.queue_name)
        channel.basic_publish('', settings.queue_name, message.__dict__)
        connection.close()
        return HTTPStatus.Ok
    except exceptions.ChannelError:
        return HTTPStatus.NOT_FOUND
