from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv("../.env")


class Base(BaseSettings):
    debug: bool = Field(True)

    send_queue_host: str = Field("127.0.0.1")
    send_queue_port: int = Field(5672)
    send_queue_username: str = Field("rabbitmq")
    send_queue_password: str = Field("rabbitmq")

    all_users_auth_url: str = Field("http://auth_service:8081/api/v1/auth/all_users/")

    queue_name: str = Field("auth_message")

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = ".env"


settings = Base()
