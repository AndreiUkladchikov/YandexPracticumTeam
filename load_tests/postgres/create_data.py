import logging
import json

import psycopg2
from models import Review
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch as _execute_batch
from fakerate import random_review
import pg_context

batch_size = 500
iterations = 2000


def main():
    count = 0
    while count < iterations:
        reviews = []
        item = 0
        while item < batch_size:
            reviews.extend([random_review()])
            item = item + 1

        with pg_context.conn_context() as conn:
            save_film_reviews(conn, reviews)

        count = count + 1
        print(count)


def save_film_reviews(conn: _connection, reviews: list[Review]) -> None:
    curr = conn.cursor()
    values = []
    sql_insert_query = """ INSERT INTO loadtest.film_rate
                            (id, rate)
                            VALUES (%s,%s) """
    for review in reviews:
        values.append(
            (
                review.id,
                json.dumps(review.__dict__, default=str)                
            )
        )
    try:
        _execute_batch(curr, sql_insert_query, values)
        conn.commit()
    except (psycopg2.Error) as error:
        logging.exception(error)
    curr.close()


if __name__ == "__main__":
    main()
