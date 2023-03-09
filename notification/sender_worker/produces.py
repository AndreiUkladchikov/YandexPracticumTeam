import json

import pika
from common.config import settings

template = {
    "email": "email@yandex.ru",
    "subject": "Welcome",
    "body": "Спасибо, что Вы с нами!",
}


cred = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=cred)
)
channel = connection.channel()
channel.queue_declare(queue=settings.send_queue)

channel.basic_publish(
    exchange="", routing_key=settings.send_queue, body=json.dumps(template).encode()
)
connection.close()
