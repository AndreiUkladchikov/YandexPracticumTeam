import os

from pydantic import BaseSettings, Field

base_dir = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    auth_db_username: str = Field(env="POSTGRES_USER")

    auth_db_password: str = Field(env="POSTGRES_PASSWORD")
    auth_db_name: str = Field(env="POSTGRES_DB")
    auth_db_host: str = Field(env="DB_HOST")
    auth_db_port: int = Field(env="DB_PORT")
    backend_host: str = ...
    backend_port: int = ...

    base_api_url: str = Field(default="/api/v1/auth")

    jwt_secret_key: str = ...

    access_token_expires_in_hours: int = Field(default=1)
    refresh_token_expires_in_days: int = Field(default=30)

    redis_host: str = ...
    redis_port: int = ...

    auth_server_host: str = ...
    auth_server_port: str = ...

    oauth_client_id: str = ...
    oauth_client_secret: str = ...

    baseurl: str = Field(default="https://oauth.yandex.ru/")
    login_url_yandex: str = Field(default="https://login.yandex.ru/info/")

    rate_limit: str = Field(default="20/minute")
    rate_limit_enabled: bool = Field(default=True)

    jaeger_tracing: bool = Field(default=False)
    jaeger_agent_host: str = Field(default="localhost")
    jaeger_logging: str = Field(default=False)

    debug_mode_handler: bool = Field(default=True)

    class Config:
        env_file = f"{base_dir}/.env"


settings = Settings()
