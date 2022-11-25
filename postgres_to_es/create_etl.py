import logging

from elasticsearch import Elasticsearch, exceptions

import config.db_config as db_config
import etl.etl_schemas as etl_schemas

es = Elasticsearch(db_config.ELASTIC_CON, timeout=300)


def main() -> None:
    create_movies()
    create_genres()


def create_movies() -> None:
    try:
        movies = etl_schemas.settings.update(etl_schemas.movies)
        es.indices.create(index='movies', body=movies)
    except exceptions.RequestError:
        logging.exception('Cannot create MOVIES schema')


def create_genres() -> None:
    try:
        genres = etl_schemas.settings.update(etl_schemas.genres)
        es.indices.create(index='genres', body=genres)
    except exceptions.RequestError:
        logging.exception('Cannot create GENRES schema')


if __name__ == '__main__':
    main()
