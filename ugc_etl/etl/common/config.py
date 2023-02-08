import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, RedisDsn, KafkaDsn

load_dotenv()


class Base(BaseSettings):

    batch_size: int = Field(100)

    redis_state_storage: RedisDsn = Field(...)

    kafka_broker: KafkaDsn = Field(...)
    kafka_group_id: str = Field(...)
    kafka_topic: str = Field(...)
    kafka_sleep_timeout: int = Field(5)

    clickhouse_dsn: str = Field(...)
    clickhouse_table: str = Field(...)

    backoff_start_sleep_time: float = Field(1.0)
    backoff_factor: int = Field(2)
    backoff_border_sleep_time: float = Field(60.0)
    backoff_try_limit: int = Field(50)

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = ".env"


settings = Base()
