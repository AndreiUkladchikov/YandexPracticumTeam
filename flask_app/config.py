from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    auth_db_username: str = Field(env="POSTGRES_USER")
    auth_db_password: str = Field(env="POSTGRES_PASSWORD")
    auth_db_name: str = Field(env="POSTGRES_DB")
    auth_db_host: str = Field(env="DB_HOST")

    jwt_secret_key: str = ...
    access_token_expires_in_seconds: int = Field(default=3600)
    refresh_token_expires_in_days: int = Field(default=30)

    class Config:
        env_file = (
            "/Users/mike/study/yandex_praktikum/YandexPracticumTeam/flask_app/.env"
        )


settings = Settings()
