import json

import pika

from common.config import settings

mail = {
    "email": "email@yandex.ru",
    "subject": "Welcome",
    "text": "Спасибо, что Вы с нами!",
    "html": "<h1>Спасибо, что Вы с нами!</h1> <br>Дорогой друг</br>",
}


def rabbit_producer(queue: str, template: dict):
    cred = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.send_queue_host, credentials=cred)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange="", routing_key=settings.send_queue, body=json.dumps(template).encode())
    connection.close()


if __name__ == "__main__":
    rabbit_producer(settings.send_queue, mail)
