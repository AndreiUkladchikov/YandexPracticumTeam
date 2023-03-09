import abc
import smtplib
from email.message import EmailMessage
from smtplib import SMTP

from common.config import settings
from loguru import logger
from retry import retry


class AbstractSender(abc.ABC):
    @abc.abstractmethod
    def send_message(self) -> int:
        """Отправляем сообщение в сервис SMTP."""
        pass


class EmailSender(AbstractSender):
    def __init__(self, email: str, subject: str, body: str, smtp_conn: smtplib.SMTP):
        self.email = email
        self.subject = subject
        self.body = body
        self.smtp_conn = smtp_conn

    def send_message(self):
        message = EmailMessage()
        message["From"] = "from@example.com"
        message["To"] = ",".join([self.email])
        message["Subject"] = self.subject

        # Для отправки HTML-письма нужно вместо метода `set_content` использовать `add_alternative` с subtype "html",
        # Иначе пользователю придёт набор тегов вместо красивого письма
        message.set_content(self.body)

        resp = self.smtp_conn.sendmail(
            message["From"], [self.email], message.as_string()
        )
        print(resp)


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
