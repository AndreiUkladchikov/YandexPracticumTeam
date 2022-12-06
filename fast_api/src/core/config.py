import os
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

    project_name: str = 'Movies'
    redis_host: str = ...
    redis_port: int = ...
    elastic_host: str = ...
    elastic_port: int = ...
    base_dir: Path = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    backend_host: str = ...
    backend_port: int = ...
    cache_expire_in_seconds: int = 100

    pagination_size: int = 50

    class Config:
        env_file = ".env"


settings = Settings()
