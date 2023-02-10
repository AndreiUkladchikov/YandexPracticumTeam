from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field(default="localhost")
    kafka_port: str = Field(default=9092)
    kafka_topic: str = Field(default="views")

    ugc_backend_host: str = Field(default="localhost")
    ugc_backend_port: int = Field(default=8080)


settings = Settings()
