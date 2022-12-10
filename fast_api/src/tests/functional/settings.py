from pydantic import BaseSettings, Field
from uuid import uuid4

class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200')
    es_index: str = Field('movies')
    es_id_field: str = Field(str(uuid4()))
    # es_index_mapping: dict =

    redis_host: str = Field('http://localhost:6379')
    service_url: str = Field('http://localhost:8008')


test_settings = TestSettings()
