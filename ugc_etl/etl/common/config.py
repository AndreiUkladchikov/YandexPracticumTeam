import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, RedisDsn, KafkaDsn

load_dotenv()


class Base(BaseSettings):
    
    BATCH_SIZE: int = Field(
        100,
        env='BATCH_SIZE',
    )
    
    REDIS_STATE_STORAGE: RedisDsn = Field(
        ...,
        env="REDIS_STATE_STORAGE",
    )
    
    KAFKA_DSN: KafkaDsn = Field(
        ...,
        env='KAFKA_DSN',
    )    
    KAFKA_WATCH_TOPIC: str = Field(
        ...,
        env='KAFKA_WATCH_TOPIC',
    )    
    KAFKA_WATCH_LATER_TOPIC: str = Field(
        ...,
        env='KAFKA_WATCH_LATER_TOPIC',
    )
    
    CLICKHOUSE_DSN: KafkaDsn = Field(
        ...,
        env='CLICKHOUSE_DSN',
    )    
    CLICKHOUSE_WATCH_TOPIC: str = Field(
        ...,
        env='CLICKHOUSE_WATCH_TABLE',
    )    
    CLICKHOUSE_WATCH_LATER_TOPIC: str = Field(
        ...,
        env='CLICKHOUSE_WATCH_LATER_TABLE',
    )

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = ".env"


settings = Base()
