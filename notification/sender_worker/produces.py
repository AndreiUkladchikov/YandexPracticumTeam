import json
from datetime import datetime
import pika

from common.config import settings

mail = {
    "email": "email@yandex.ru",
    "subject": "Welcome",
    "text": "Спасибо, что Вы с нами!",
    "html": "<h1>Спасибо, что Вы с нами!</h1> <br>Дорогой друг</br>",
}

change_password = {
    "email": "bary@yandex.ru",
    "subject": "Change password",
    "text": "Вы сменили пароль. Уважаемый пользователь! "
    "Если вы этого не делали, то необходимо срочно обратиться в службу поддержки",
    "html": "<h1>Смена пароля {}</h1> <br>Уважаемый пользователь!"
    " Если вы этого не делали, то необходимо срочно обратиться в службу поддержки</br>".format(
        datetime.now()
    ),
}


def rabbit_producer(queue: str, template: dict[str, str]):
    """
    Функция для тестовой отправки писем (mail, change_password) в очередь
    :param queue: название очереди
    :param template: сообщение
    :return:
    """
    cred = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.send_queue_host, credentials=cred)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange="", routing_key=settings.send_queue, body=json.dumps(template).encode())
    connection.close()


if __name__ == "__main__":
    rabbit_producer(settings.send_queue, change_password)
