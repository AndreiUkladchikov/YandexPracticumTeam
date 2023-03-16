import json

import pika
from loguru import logger
from pika.exceptions import ConnectionClosedByBroker
from retry import retry

from common.config import settings


@retry()
def rabbit_consumer(username: str, password: str, queue: str, host: str):
    cred = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, credentials=cred)
    )
    channel = connection.channel()

    channel.queue_declare(queue=settings.send_queue)
    while True:
        try:
            logger.info(" [*] Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()
            for method, properties, body in channel.consume(queue=queue, auto_ack=True):
                yield json.loads(body)

        except (
            pika.exceptions.ConnectionClosedByBroker,
            pika.exceptions.AMQPChannelError,
        ) as e:
            logger.exception(e)
            break

        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            logger.info(pika.exceptions.AMQPConnectionError)
            continue

        finally:
            channel.stop_consuming()
