import json

import pika
from loguru import logger
from pika.exceptions import ConnectionClosedByBroker
from retry import retry

from common.config import settings


class RabbitHandler:
    def __init__(self, username, password, host):
        cred = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=cred))
        self.channel = connection.channel()

    def producer(self):
        pass

    @retry
    def consumer(self, queue):
        self.channel.queue_declare(queue=settings.send_queue)
        while True:
            try:
                logger.info(" [*] Waiting for messages. To exit press CTRL+C")
                self.channel.start_consuming()
                # channel.basic_consume(queue=settings.send_queue, on_message_callback=catch_callback, auto_ack=True)
                for method, properties, body in self.channel.consume(queue=queue, auto_ack=True):
                    yield json.loads(body)

            # Don't recover if connection was closed by broker
            except pika.exceptions.ConnectionClosedByBroker:
                logger.exception(pika.exceptions.ConnectionClosedByBroker)
                break
            # Don't recover on channel errors
            except pika.exceptions.AMQPChannelError:
                logger.exception(pika.exceptions.AMQPChannelError)
                break
            # Recover on all other connection errors
            except pika.exceptions.AMQPConnectionError:
                logger.info(pika.exceptions.AMQPConnectionError)
                continue


@retry()
def rabbit_consumer():
    cred = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.send_queue_host, credentials=cred)
    )
    channel = connection.channel()

    channel.queue_declare(queue=settings.send_queue)
    while True:
        try:
            logger.info(" [*] Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()
            # channel.basic_consume(queue=settings.send_queue, on_message_callback=catch_callback, auto_ack=True)
            for method, properties, body in channel.consume(queue=settings.send_queue, auto_ack=True):
                yield json.loads(body)

        # Don't recover if connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker:
            logger.exception(pika.exceptions.ConnectionClosedByBroker)
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError:
            logger.exception(pika.exceptions.AMQPChannelError)
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            logger.info(pika.exceptions.AMQPConnectionError)
            continue
