import pg_context as pg_context
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch as _execute_batch


def main():
    with pg_context.conn_context() as conn:
        create_db(conn)


def create_db(conn: _connection) -> None:
    curr = conn.cursor()
    sql_query = """CREATE SCHEMA IF NOT EXISTS loadtest;"""
    curr.execute(sql_query)
    curr.execute(open("document_database.sql", "r").read())
    conn.commit()
    curr.close()


if __name__ == "__main__":
    main()
