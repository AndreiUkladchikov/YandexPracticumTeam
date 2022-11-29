import os
from pydantic import BaseSettings, Field

# For local debug
# from dotenv import load_dotenv
# load_dotenv()


STATE_CON = os.environ.get('STATE_CON')

ELASTIC_CON = os.environ.get('ELASTIC_CON')


class PostgresSettings(BaseSettings):
    dbname: str = Field(default=os.environ.get('DB_NAME'))
    user: str = Field(default=os.environ.get('POSTGRES_USER'))
    password: str = Field(default=os.environ.get('POSTGRES_PASSWORD'))
    host: str = Field(default=os.environ.get('DB_HOST'))
    port: str = Field(default=os.environ.get('DB_PORT'))

    class Config:
        env_file = '.env'
