from contextlib import contextmanager

import db_config
import psycopg2


@contextmanager
def conn_context():
    conn = psycopg2.connect(**db_config.POSTGRES_CON)
    yield conn
    conn.close()
