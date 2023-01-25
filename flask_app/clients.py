from contextlib import contextmanager

import requests
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from base import BaseClient
from config import settings

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class PostgresClient(BaseClient):
    def __init__(self, db_host: str, db_name: str, db_username: str, db_password: str):
        self.engine = create_engine(
            f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}",
            convert_unicode=True,
        )

        self.base = declarative_base()
        self.base.metadata = metadata

    def get_base(self):
        return self.base

    @contextmanager
    def get_session(self):
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def create_all_tables(self):
        import db_models

        self.base.metadata.create_all(self.engine)


class HttpClient(BaseClient):
    @contextmanager
    def get_session(self) -> requests.Session:
        session = requests.Session()
        yield session
        session.close()


postgres_client = PostgresClient(
    db_host=settings.auth_db_host,
    db_name=settings.auth_db_name,
    db_username=settings.auth_db_username,
    db_password=settings.auth_db_password,
)
