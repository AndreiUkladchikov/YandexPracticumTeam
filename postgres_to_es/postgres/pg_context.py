from contextlib import contextmanager

from db_config import PostgresSettings
import psycopg2


@contextmanager
def conn_context():
    conn = psycopg2.connect(str(PostgresSettings()))
    yield conn
    conn.close()
