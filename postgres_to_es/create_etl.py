import config.db_config as db_config
import etl.etl_schemas as etl_schemas
from elasticsearch import Elasticsearch, exceptions
from loguru import logger

es = Elasticsearch(db_config.ELASTIC_CON)


def main() -> None:
    create_indexes()


def create_indexes() -> None:
    create_movies()
    create_genres()
    create_persons()


def create_movies() -> None:
    try:
        movies = etl_schemas.settings
        movies.update(etl_schemas.movies)
        es.indices.create(index="movies", body=movies)
    except exceptions.RequestError:
        logger.exception("Cannot create MOVIES schema")


def create_genres() -> None:
    try:
        genres = etl_schemas.settings
        genres.update(etl_schemas.genres)
        es.indices.create(index="genres", body=genres)
    except exceptions.RequestError:
        logger.exception("Cannot create GENRES schema")


def create_persons() -> None:
    try:
        persons = etl_schemas.settings
        persons.update(etl_schemas.persons)
        es.indices.create(index="persons", body=persons)
    except exceptions.RequestError:
        logger.exception("Cannot create PERSONS schema")


if __name__ == "__main__":
    main()
