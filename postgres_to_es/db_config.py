import os
from pydantic import BaseSettings


STATE_CON = os.environ.get('STATE_CON')

ELASTIC_CON = os.environ.get('ELASTIC_CON')


class PostgresSettings(BaseSettings):
    dbname: str
    user: str
    password: str
    host: str
    port: str

    class Config:
        env_file = '.env'
