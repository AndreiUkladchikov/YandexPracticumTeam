import os
import sys

from loguru import logger

from common.config import settings
from consumer import RabbitHandler, rabbit_consumer
from sender import EmailSender, SMTPConnection

if __name__ == "__main__":
    smtp_conn = SMTPConnection(settings.smtp_host, settings.smtp_port)
    connection = smtp_conn.create_connection()
    handler = RabbitHandler(
        settings.send_queue_username,
        settings.send_queue_password,
        settings.send_queue_host,
    )

    try:
        for mail in rabbit_consumer():
            if not smtp_conn.test_conn_open():
                new_smtp_conn = SMTPConnection(settings.smtp_host, settings.smtp_port)
                connection = new_smtp_conn.create_connection()
            sender = EmailSender(email=mail, smtp_conn=connection)
            sender.send_message()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
