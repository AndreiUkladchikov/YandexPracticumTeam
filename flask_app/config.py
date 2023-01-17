import os
from pydantic import BaseSettings, Field

base_dir = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    auth_db_username: str = Field(env="POSTGRES_USER")
    auth_db_password: str = Field(env="POSTGRES_PASSWORD")
    auth_db_name: str = Field(env="POSTGRES_DB")
    auth_db_host: str = Field(env="DB_HOST")

    jwt_secret_key: str = ...

    access_token_expires_in_hours: int = Field(default=1)
    refresh_token_expires_in_days: int = Field(default=30)

    redis_host: str = ...
    redis_port: int = ...

    class Config:
        env_file = (
            f"{base_dir}/.env"
        )


settings = Settings()
