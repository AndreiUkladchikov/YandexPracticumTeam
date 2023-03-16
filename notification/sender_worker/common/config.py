from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv("../.env")

RABBIT_PORT = 5672
SMTP_PORT = 1025


class Base(BaseSettings):
    debug: bool = Field(True)

    send_queue_host: str = Field("127.0.0.1")
    send_queue_port: int = Field(5672)
    send_queue_username: str = Field("rabbitmq")
    send_queue_password: str = Field("rabbitmq")

    send_queue: str = Field("send_auth_message")
    death_queue: str = Field("death_queue")

    backoff_start_sleep_time: float = Field(1)
    backoff_factor: int = Field(2)
    backoff_border_sleep_time: float = Field(60)
    backoff_try_limit: int = Field(10)

    smtp_host: str = Field("localhost")
    smtp_port: int = Field(1025)

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = ".env"


settings = Base()
