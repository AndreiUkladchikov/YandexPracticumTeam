import time
from typing import Any

import logging
import etl.etl_save as etl_save
import psycopg2
import elasticsearch

import postgres.load_data as load_data
import postgres.pg_context as pg_context
import services.state_worker as state_worker
from config.config_models import State, Indexes
import config.db_config as db_config


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
    state = state_worker.get_state(db_config.STATE_CON)
    if state.is_finished is True:
        state = state_worker.refresh_state(db_config.STATE_CON, state)
    while True:
        state = etl_worker(state)
        if state.is_finished:
            time.sleep(etl_update_frequency)
            state = state_worker.refresh_state(db_config.STATE_CON, state)


def etl_worker(state: State) -> State:
    while state.is_finished is False:
        data = load(state)
        if len(data) > 0:
            save(data, state.index)
            state.last_row = state.last_row + len(data)
        else:
            state = state_worker.get_next_state(state)
        state_worker.save_state(db_config.STATE_CON, state)
        return state


@backoff(exception=psycopg2.OperationalError)
def load(state: State) -> list[Any]:
    with pg_context.conn_context(str(db_config.PostgresSettings())) as conn:
        if state.index == Indexes.MOVIE.value:
            data = load_data.load_film_works(conn, state.last_update, state.last_row, limit)
        elif state.index == Indexes.GENRE.value:
            data = load_data.load_genres(conn, state.last_update, state.last_row, limit)
        else:
            data = []
        return data


@backoff(exception=elasticsearch.exceptions.RequestError)
def save(source: list[Any], index: str) -> None:
    data = []
    for item in source:
        json = item.json()
        data.append({
            "_id": item.id,
            "_index": index,
            "_source": json
        })
    etl_save.put_data(db_config.ELASTIC_CON, data)


if __name__ == '__main__':
    main()
