import os
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

base_dir: Path = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    """
    PROJECT_NAME: Название проекта. Используется в Swagger-документации
    REDIS_HOST, REDIS_PORT: Настройки Redis
    ELASTIC_HOST, ELASTIC_PORT: Настройки Elasticsearch
    BASE_DIR: Корень проекта
    """

    project_name: str = "Movies"
    redis_host: str = ...
    redis_port: int = ...
    elastic_host: str = ...
    elastic_port: int = ...

    backend_host: str = ...
    backend_port: int = ...
    cache_expire_in_seconds: int = 100

    pagination_size: int = 50

    max_page_size: int = 10000
    max_page_number: int = 200

    class Config:
        env_file = f"{base_dir}/.env"


settings = Settings()
