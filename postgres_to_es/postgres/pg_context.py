from contextlib import contextmanager

import psycopg2


@contextmanager
def conn_context(conn: str):
    conn = psycopg2.connect(conn)
    yield conn
    conn.close()
