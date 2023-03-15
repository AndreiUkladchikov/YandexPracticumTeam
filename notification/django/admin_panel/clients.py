from http import HTTPStatus

import pika
import requests
from pika import exceptions

from admin_panel.config import settings


class HttpClient:
    def __get(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def get_all_user_ids(self, url, **kwargs):
        response = self.__get(url, **kwargs)
        list_of_ids = [user.get('user_id') for user in response.json().get('result')]
        return list_of_ids


class RabbitClient:
    def __init__(self):
        self.cred = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.send_queue_host, credentials=self.cred)
        )

    def __del__(self):
        self.connection.close()

    def send_message(self, message):
        try:
            channel = self.connection.channel()
            channel.queue_declare(queue=settings.queue_name)
            channel.basic_publish('', settings.queue_name, message.__dict__)
            return HTTPStatus.OK
        except exceptions.ChannelError:
            return HTTPStatus.NOT_FOUND
