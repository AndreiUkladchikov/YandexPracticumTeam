from dotenv import load_dotenv
from pydantic import BaseSettings, Field, KafkaDsn, RedisDsn

load_dotenv('../.env')


class Base(BaseSettings):
    debug: bool = Field(True)

    messages_queue_host: str = Field('127.0.0.1')
    messages_queue_port: int = Field(5672)
    messages_queue_username: str = Field('rabbitmq')
    messages_queue_password: str = Field('rabbitmq')
    messages_queue: str = Field('auth_message')

    send_queue_host: str = Field('127.0.0.1')
    send_queue_port: int = Field(5672)
    send_queue_username: str = Field('rabbitmq')
    send_queue_password: str = Field('rabbitmq')
    send_queue: str = Field('send_auth_message')

    auth_service_bearer_token: str = Field(...)

    user_info_url: str = Field('http://127.0.0.1:8081/v1/user/')
    film_info_url: str = Field('http://127.0.0.1:8080/v1/film/')

    backoff_start_sleep_time: float = Field(1)
    backoff_factor: int = Field(2)
    backoff_border_sleep_time: float = Field(60)
    backoff_try_limit: int = Field(10)

    test_user_id: str = Field('775f21b1-3a1c-45cd-9495-e1cab2418277')
    test_film_id: str = Field('7303d55d-cca1-46e5-9d4e-69f11117816f')

    test_user_email: str = Field('testuser@test.loc')
    test_user_firstname: str = Field('John')
    test_film_title: str = Field('')
    test_film_rate: float = Field(9.9)

    class Config:
        case_sensitive = False
        env_file_encoding = 'utf-8'
        env_file = '.env'


settings = Base()
