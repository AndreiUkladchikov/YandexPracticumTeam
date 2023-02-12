from clickhouse_driver import Client

client = Client(host='localhost') 


def create_db() -> None:
    client.execute('CREATE DATABASE IF NOT EXISTS movies ON CLUSTER company_cluster')
    create_db_tables()


def create_db_tables() -> None:
    client.execute(
        'CREATE TABLE movies.watch_history ON CLUSTER company_cluster (id Int64, user_id String, film_id String, timestamp Int32) Engine=MergeTree() ORDER BY id'
    )


def insert_data(data) -> None:
    client.execute('INSERT INTO movies.watch_history (user_id, film_id, timestamp) VALUES', data)


def count_rows() -> int:
    return client.execute('SELECT count() from movies.watch_history')


def read_rows():
    client.execute('SELECT * from movies.watch_history WHERE timestamp = 12345678')


if __name__ == "__main__":
    create_db()
