from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    auth_db_username: str = Field(env="POSTGRES_USER")
    auth_db_password: str = Field(env="POSTGRES_PASSWORD")
    auth_db_name: str = Field(env="POSTGRES_DB")
    auth_db_host: str = Field(env="DB_HOST")

    jwt_secret_key: str = ...

    class Config:
        env_file = ".env"


settings = Settings()
