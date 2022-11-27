import os
from pydantic import BaseSettings, Field
from ipaddress import IPv4Address
from logging import config as logging_config
from pathlib import Path
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
    REDIS_HOST: IPv4Address = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)
    ELASTIC_HOST: IPv4Address = Field(default="127.0.0.1")
    ELASTIC_PORT: int = Field(default=9200)
    BASE_DIR: Path = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    BACKEND_HOST: IPv4Address = Field(default="0.0.0.0")
    BACKEND_PORT: int = Field(default=8008)
