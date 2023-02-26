from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field(...)
    kafka_port: str = Field(default=9092)
    kafka_topic: str = Field(default="views")

    ugc_backend_host: str = Field(default="0.0.0.0")
    ugc_backend_port: int = Field(default=8080)

    sentry_url: str = Field(...)
    sentry_traces_sample_rate: float = Field(0.05)

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = "../.env"


settings = Settings()
