import logging
import time

import psycopg2

import pg_context as pg_context
from psycopg2.extensions import connection as _connection
from psycopg2.extras import NamedTupleCursor
from create_data import save_film_reviews
from fakerate import random_review

test_count = 10


def main():
    count = 0
    while count < test_count:
        review = random_review()
        reviews = []
        reviews.extend([review])
        test_write(reviews)        
        test_read(review.id)
        count = count + 1


def test_write(reviews):
    start = time.perf_counter()
    with pg_context.conn_context() as conn:
        save_film_reviews(conn, reviews)   
    end = time.perf_counter() 
    speed = (end - start) * 10 ** 3
    logging.info(f'Write 1 row in {speed:.03f} ms')


def test_read(id):
    start = time.perf_counter()
    with pg_context.conn_context() as conn:
        try:
            curs = conn.cursor(cursor_factory=NamedTupleCursor)
            curs.execute(f"SELECT * FROM loadtest.film_rate WHERE id='{id}';")
            result = curs.fetchall()        
        except (psycopg2.Error) as error:
            logging.error(error)
    end = time.perf_counter() 
    speed = (end - start) * 10 ** 3
    logging.info(f'Read 1 row in {speed:.03f} ms')


if __name__ == "__main__":
    main()
