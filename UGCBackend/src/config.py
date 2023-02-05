from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field(default="localhost")
    kafka_port: str = Field(default=9092)
    kafka_topic: str = Field(default="views")

    ugc_backend_host: str = Field(default="localhost")
    ugc_backend_port: int = Field(default=8092)

    film_service_host: str = Field(default="localhost")
    film_service_port: str = Field(default=8008)

    time_cache_expired: int = Field(default=20)

    class Config:
        env_file = "./env"


settings = Settings()
