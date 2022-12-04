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

    PROJECT_NAME: str = Field(default=os.environ.get('PROJECT_NAME'))
    REDIS_HOST: str = Field(default=os.environ.get('REDIS_HOST'))
    REDIS_PORT: int = Field(default=os.environ.get('REDIS_PORT'))
    ELASTIC_HOST: str = Field(default=os.environ.get('ELASTIC_HOST'))
    ELASTIC_PORT: int = Field(default=os.environ.get('ELASTIC_PORT'))
    BASE_DIR: Path = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    BACKEND_HOST: IPv4Address = Field(default=os.environ.get('BACKEND_HOST'))
    BACKEND_PORT: int = Field(default=os.environ.get('BACKEND_PORT'))
    CACHE_EXPIRE_IN_SECONDS: int = Field(default=100)

    PAGINATION_SIZE: int = Field(default=50)

    class Config:
        env_file = ".env"


settings = Settings()
