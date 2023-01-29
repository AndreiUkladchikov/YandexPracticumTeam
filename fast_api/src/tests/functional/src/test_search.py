import http

import pytest
from functional.config import test_settings
from functional.testdata.data_main_page import cache_films_main_page
from functional.testdata.data_search import test_data_films
from functional.utils.helpers import make_get_request


@pytest.mark.asyncio
async def test_cache_after_delete(es_write_data, es_delete_data):
    await es_write_data(test_data_films, test_settings.movie_index)
    await es_write_data(cache_films_main_page, test_settings.movie_index)

    query_data = "Test film"
    response = await make_get_request("films/search", query_data)
    assert response.status == http.HTTPStatus.OK
    await es_delete_data(test_settings.movie_index)

    response = await make_get_request("films/search", query_data)
    assert response.status == http.HTTPStatus.OK


@pytest.mark.asyncio
class TestSearch:
    async def test_search(self, set_up_search_films):
        query_data = "Test film"

        response = await make_get_request("films/search", query_data)

        assert response.status == http.HTTPStatus.OK
        assert response.body["films"][0]["title"] == query_data

    async def test_search_paging_first_page(self, set_up_search_films):
        query_data = "First film"
        page_number = 1
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == http.HTTPStatus.OK
        assert len(response.body["films"]) == page_size

    async def test_search_paging_last_page(self, set_up_search_films):
        query_data = "First film"
        page_number = 3
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == http.HTTPStatus.OK
        assert len(response.body["films"]) == 10

    async def test_validate_page_size(self, set_up_search_films):
        query_data = "Test film"
        page_number = 1
        page_size = -40

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_select_page_more_than_exists(self, set_up_search_films):
        # Граничное условие. Тестируем 100 страницу
        query_data = "Test film"
        page_number = 100
        page_size = 50
        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == http.HTTPStatus.NOT_FOUND

    async def test_validate_page_number(self, set_up_search_films):
        query_data = "Test film"
        page_number = "hello"
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY
