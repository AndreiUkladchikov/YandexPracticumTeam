from uuid import uuid4

from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://elastic:9200')
    movie_index: str = Field('movies')
    genre_index: str = Field('genres')
    person_index: str = Field('persons')

    es_id_field: str = Field(str(uuid4()))

    redis_host: str = Field('http://redis:6379')
    service_url: str = Field('http://nginx:8080')


test_settings = TestSettings()
