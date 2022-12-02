import os
from ipaddress import IPv4Address
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    """
    PROJECT_NAME: Название проекта. Используется в Swagger-документации
    REDIS_HOST, REDIS_PORT: Настройки Redis
    ELASTIC_HOST, ELASTIC_PORT: Настройки Elasticsearch
    BASE_DIR: Корень проекта
    """

    PROJECT_NAME: str = Field(default="movies")
    REDIS_HOST: str = Field(default="redis")
    REDIS_PORT: int = Field(default=6379)
    ELASTIC_HOST: str = Field(default="elastic")
    ELASTIC_PORT: int = Field(default=9200)
    BASE_DIR: Path = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    BACKEND_HOST: IPv4Address = Field(default="0.0.0.0")
    BACKEND_PORT: int = Field(default=8008)
    CACHE_EXPIRE_IN_SECONDS: int = Field(default=1)

    PAGINATION_SIZE: int = Field(default=50)

    class Config:
        env_file = ".env"


settings = Settings()
