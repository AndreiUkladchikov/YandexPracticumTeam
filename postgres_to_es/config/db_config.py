import os

from pydantic import BaseSettings, Field

# For local debug
# from dotenv import load_dotenv
# load_dotenv()
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATE_CON = os.environ.get("STATE_CON")

ELASTIC_CON = os.environ.get("ELASTIC_CON")


class PostgresSettings(BaseSettings):
    dbname: str = Field(env="DB_NAME")
    user: str = Field(env="POSTGRES_USER")
    password: str = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="DB_HOST")
    port: str = Field(env="DB_PORT")

    class Config:
        env_file = f"{base_dir}/.env"
