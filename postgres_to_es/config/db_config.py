import os
from pydantic import BaseSettings, Field

# For local debug
# from dotenv import load_dotenv
# load_dotenv()


STATE_CON = os.environ.get('STATE_CON', 'state.json')

ELASTIC_CON = os.environ.get('ELASTIC_CON', 'http://localhost:9200')


class PostgresSettings(BaseSettings):
    dbname: str = Field(default="movies_database")
    user: str = Field(default="app")
    password: str = Field(default="123qwe")
    host: str = Field(default="localhost")
    port: str = Field(default="5432")

    class Config:
        env_file = '.env'
