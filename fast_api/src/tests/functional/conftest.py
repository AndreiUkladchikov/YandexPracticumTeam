import asyncio

import pytest
from elasticsearch import AsyncElasticsearch, helpers
from config import test_settings
from testdata.data_search import test_data_films
from testdata.data_main_page import (
    test_main_page_genres,
    test_films_main_page,
)
from testdata.data_genres import test_genres
from testdata.data_persons import test_film_by_person, test_persons


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data, index):
        bulk_query = get_es_bulk_query(data, index)
        await helpers.async_bulk(es_client, bulk_query, refresh="wait_for")

    return inner


@pytest.fixture(scope="class")
def es_delete_data(es_client: AsyncElasticsearch):
    async def inner(index):
        response = await es_client.delete_by_query(
            index=index, body={"query": {"match_all": {}}}
        )

    return inner


@pytest.fixture(scope="class")
async def set_up_search_films(es_write_data, es_delete_data):
    await es_write_data(test_data_films, test_settings.movie_index)
    yield es_client
    await es_delete_data(test_settings.movie_index)


@pytest.fixture(scope="class")
async def set_up_main_page(es_write_data, es_delete_data):
    await es_write_data(test_films_main_page, test_settings.movie_index)
    await es_write_data(test_main_page_genres, test_settings.genre_index)

    yield es_client

    await es_delete_data(test_settings.movie_index)
    await es_delete_data(test_settings.genre_index)


@pytest.fixture(scope="class")
async def set_up_genres(es_write_data, es_delete_data):
    await es_write_data(test_genres, test_settings.genre_index)
    yield es_client
    await es_delete_data(test_settings.genre_index)


@pytest.fixture(scope="class")
async def set_up_persons(es_write_data, es_delete_data):
    await es_write_data(test_persons, test_settings.person_index)
    await es_write_data(test_film_by_person, test_settings.movie_index)
    yield es_client
    await es_delete_data(test_settings.person_index)
    await es_delete_data(test_settings.movie_index)


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await client.close()


def get_es_bulk_query(es_data: list, index: str):
    data = []
    for item in es_data:
        data.append({"_id": item["id"], "_index": index, "_source": item})
    return data
