from pydantic import BaseSettings, Field, MongoDsn


class Settings(BaseSettings):
    kafka_host: str = Field(default="localhost")
    kafka_port: str = Field(default=9092)
    kafka_topic: str = Field(default="views")

    ugc_backend_host: str = Field(default="0.0.0.0")
    ugc_backend_port: int = Field(default=8080)

    mongo: MongoDsn = Field(default="mongodb://localhost:27017")

    max_page_number: int = Field(default=1000)
    max_page_size: int = Field(default=50)

    mongo_db: str = Field(default="myNewDB")
    like_collection: str = Field(default="films")
    reviews_collection: str = Field(default="reviews")
    bookmarks_collection: str = Field(default="bookmarks")

    logstash_host: str = Field(default="localhost")
    logstash_port: int = Field(default=5044)

    sentry_url: str = Field(...)
    sentry_traces_sample_rate: float = Field(0.05)

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_file = "../.env"


settings = Settings()
