import os
import sys
from smtplib import SMTP

from common.config import settings
from consumer import rabbit_consumer
from loguru import logger
from retry import retry
from sender import EmailSender, SMTPConnection

# def test_conn_open(conn):
#     try:
#         status = conn.noop()[0]
#     except :  # smtplib.SMTPServerDisconnected
#         status = -1
#     return True if status == 250 else False


# @retry(backoff=settings.backoff_factor, logger=logger)
# def create_connection(host, port):
#     return SMTP(host, port)


if __name__ == "__main__":
    smtp_conn = SMTPConnection(settings.smtp_host, settings.smtp_port)
    connection = smtp_conn.create_connection()
    try:
        for mail in rabbit_consumer():
            if not smtp_conn.test_conn_open():
                new_smtp_conn = SMTPConnection(settings.smtp_host, settings.smtp_port)
                connection = new_smtp_conn.create_connection()
            sender = EmailSender(
                email=mail["email"],
                subject=mail["subject"],
                body=mail["body"],
                smtp_conn=connection,
            )
            sender.send_message()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
