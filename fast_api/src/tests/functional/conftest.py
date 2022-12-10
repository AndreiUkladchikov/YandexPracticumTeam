import pytest
from tests.functional.settings import test_settings
from elasticsearch import AsyncElasticsearch, helpers, Elasticsearch
from dataclasses import dataclass
import aiohttp


@pytest.fixture
def es_delete_data(es_client: AsyncElasticsearch):
    async def inner(index):
        response = await es_client.delete_by_query(index=index,
                                                   body={"query": {"match_all": {}}})
    return inner


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index: str):
        bulk_query = get_es_bulk_query(data, index)
        response = await helpers.async_bulk(es_client, bulk_query, refresh='wait_for')
    return inner


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await client.close()


def get_es_bulk_query(es_data, index):
    data = []
    for item in es_data:
        data.append({"_id": item["id"], "_index": index, "_source": item})
    return data


@dataclass
class Response:
    body: list[dict]
    status: int


@pytest.fixture
def make_get_request():
    async def inner(end_of_url, query: str, page_number: int, page_size: int) -> Response:
        session = aiohttp.ClientSession()
        url = test_settings.service_url + "/api/v1/" + str(end_of_url)
        query_data = {"query": str(query), 'page[number]': page_number, 'page[size]': page_size}
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        return Response(body=body, status=status)

    return inner
