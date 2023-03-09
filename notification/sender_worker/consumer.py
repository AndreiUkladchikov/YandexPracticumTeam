import json

import pika
from common.config import settings
from pika.exceptions import ConnectionClosedByBroker
from retry import retry


@retry()
def rabbit_consumer():
    while True:
        try:
            cred = pika.PlainCredentials(
                settings.send_queue_username, settings.send_queue_password
            )
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.send_queue_host, credentials=cred
                )
            )
            channel = connection.channel()

            channel.queue_declare(queue=settings.send_queue)

            print(" [*] Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()
            # channel.basic_consume(queue=settings.send_queue, on_message_callback=catch_callback, auto_ack=True)
            for method, properties, body in channel.consume(
                queue=settings.send_queue, auto_ack=True
            ):
                yield json.loads(body)

        # Don't recover if connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker:
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError:
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            continue
