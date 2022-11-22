import time

import logging
import elastic
import elasticsearch
import psycopg2

import postgres.load_data as load_data
import postgres.pg_context as pg_context
import state_worker
from config_models import State
from models import Movie


"""
etl_update_frequency - частота обновления данных (сек)
limit - количество записей для загрузки пачкой (bulk)
"""

etl_update_frequency = 60
limit = 20


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, exception: Exception = None):
    def func_wrapper(func):
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            repeat = True
            while repeat:
                try:
                    result = func(*args, **kwargs)
                    repeat = False
                    return result
                except exception:
                    logging.exception(func.__name__)
                    if sleep_time < border_sleep_time:
                        sleep_time = sleep_time * factor
                    time.sleep(sleep_time)
        return inner
    return func_wrapper


def main():
    state = state_worker.get_state()
    if state.is_finished is True:
        state = state_worker.refresh_state(state)
    while True:
        state = etl_worker(state)
        if state.is_finished:
            time.sleep(etl_update_frequency)
            state = state_worker.refresh_state(state)


def etl_worker(state: State) -> State:
    while state.is_finished is False:
        movies = load_movies(state)
        if len(movies):
            save_movies(movies)
            state.last_row = state.last_row + len(movies)
        else:
            state.is_finished = True
        state_worker.save_state(state)
        return state


@backoff(exception=psycopg2.OperationalError)
def load_movies(state: State) -> list[Movie]:
    with pg_context.conn_context() as conn:
        movies = load_data.load_film_works(conn, state.last_update, state.last_row, limit)
        return movies


@backoff(exception=elasticsearch.ElasticsearchException)
def save_movies(movies: list[Movie]) -> None:
    data = []
    for movie in movies:
        json = movie.json()
        data.append({
            "_id": movie.id,
            "_index": "movies",
            "_source": json
        })
    elastic.put_data(data)


if __name__ == '__main__':
    main()
