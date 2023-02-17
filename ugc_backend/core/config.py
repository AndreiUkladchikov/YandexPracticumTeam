from pydantic import BaseSettings, Field, MongoDsn


class Settings(BaseSettings):
    kafka_host: str = Field(...)
    kafka_port: str = Field(default=9092)
    kafka_topic: str = Field(default="views")

    ugc_backend_host: str = Field(default="0.0.0.0")
    ugc_backend_port: int = Field(default=8080)

    mongo: MongoDsn = Field(default="mongodb://localhost:27017")

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = "../.env"


settings = Settings()
