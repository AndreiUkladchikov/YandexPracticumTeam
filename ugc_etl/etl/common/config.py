from dotenv import load_dotenv
from pydantic import BaseSettings, Field, RedisDsn, KafkaDsn

load_dotenv()


class Base(BaseSettings):

    batch_size: int = Field(1000000)

    redis_storage: RedisDsn = Field(...)
    redis_list_key: str = Field(...)

    kafka_broker: KafkaDsn = Field(...)
    kafka_group_id: str = Field(...)
    kafka_topic: str = Field(...)
    kafka_sleep_timeout: int = Field(5)

    clickhouse_host: str = Field(...)

    backoff_start_sleep_time: float = Field(1.0)
    backoff_factor: int = Field(2)
    backoff_border_sleep_time: float = Field(60.0)
    backoff_try_limit: int = Field(50)

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = ".env"


settings = Base()
