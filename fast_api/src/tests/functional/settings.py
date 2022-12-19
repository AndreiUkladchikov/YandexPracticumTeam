from pydantic import BaseSettings, Field
from uuid import uuid4


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200')
    movie_index: str = Field('movies')
    genre_index: str = Field('genres')
    person_index: str = Field('persons')

    es_id_field: str = Field(str(uuid4()))

    redis_host: str = Field('http://localhost:6379')
    service_url: str = Field('http://localhost:8080')


test_settings = TestSettings()
