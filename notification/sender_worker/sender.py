import abc
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from loguru import logger
from retry import retry

from common.config import settings
from produces import rabbit_producer


class AbstractSender(abc.ABC):
    @abc.abstractmethod
    def send_message(self) -> int:
        pass


class EmailSender(AbstractSender):
    def __init__(self, email: dict, smtp_conn: smtplib.SMTP):
        self.email = email
        self.smtp_conn = smtp_conn

    def send_message(self):
        message = MIMEMultipart("alternative")
        message["From"] = "from@example.com"
        message["To"] = ",".join([self.email.get("email")])
        message["Subject"] = self.email.get("subject")
        message.attach(MIMEText(self.email.get("text"), "plain"))
        message.attach(MIMEText(self.email.get("html"), "html"))

        try:
            self.smtp_conn.sendmail(
                message.get("From"),
                message.get("To"),
                message.as_string(),
            )
            logger.info(message.as_string())
        except (smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused) as exc:
            logger.exception(exc)
            rabbit_producer(settings.death_queue, self.email)


class SMTPConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = self.create_connection()

    def test_conn_open(self):
        try:
            status = self.conn.noop()[0]
        except smtplib.SMTPServerDisconnected:
            status = -1
        return True if status == 250 else False

    @retry(
        backoff=settings.backoff_factor,
        delay=settings.backoff_start_sleep_time,
        max_delay=settings.backoff_border_sleep_time,
        logger=logger,
    )
    def create_connection(self):
        return SMTP(self.host, self.port)
