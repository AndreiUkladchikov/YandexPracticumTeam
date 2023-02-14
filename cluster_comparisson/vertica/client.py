import vertica_python


connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
} 


def create_table():
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE movies_history (user_id VARCHAR, film_id VARCHAR, timestamp INT)") 
        connection.commit()


def insert_rows(data):
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.executemany("INSERT INTO movies_history(user_id, film_id, timestamp) VALUES (?, ?, ?)", data, use_prepared_statements=True) 
        connection.commit()


def count_rows() -> int:
    result = 0
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) from movies_history")
        result = cursor.fetchone()
        connection.commit()
    return result[0]


def read_rows(timestamp: int):
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from movies_history WHERE timestamp={timestamp} LIMIT 1")
        cursor.fetchall()
        connection.commit()


if __name__ == "__main__":
    create_table()
