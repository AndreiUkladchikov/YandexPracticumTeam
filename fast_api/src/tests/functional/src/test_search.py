import pytest
from tests.functional.settings import test_settings
from tests.functional.testdata.data import test_data_films
#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором
#  `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

pytestmark = pytest.mark.asyncio


async def test_search_no_films_in_es(make_get_request):
    query_data = "Test film"
    response = await make_get_request("films/search", query_data)
    assert response.status == 404

    response = await make_get_request("films/search/vkrltmb", query_data)
    assert response.status == 404


async def test_cache_after_delete_index_in_es(make_get_request, es_write_data, es_delete_data):
    await es_write_data(test_data_films, test_settings.es_index)
    query_data = "Test film"
    response = await make_get_request("films/search", query_data)
    assert response.status == 200

    await es_delete_data(test_settings.es_index)

    response = await make_get_request("films/search", query_data)
    assert response.status == 200


@pytest.mark.asyncio
class TestSearch:
    async def test_search(self, make_get_request, setUp):
        query_data = "Test film"

        # 4. Проверяем ответ
        response = await make_get_request("films/search", query_data)

        assert response.status == 200
        assert response.body[0]["title"] == query_data

    async def test_search_paging_first_page(self, make_get_request, setUp):
        query_data = "Test film"
        page_number = 1
        page_size = 20

        # 4. Проверяем ответ
        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == 200
        assert len(response.body) == page_size

    async def test_search_paging_last_page(self, make_get_request, setUp):
        query_data = "Test film"
        page_number = 3
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == 200
        assert len(response.body) == 10

    async def test_validate_page_size(self, make_get_request, setUp):
        query_data = "Test film"
        page_number = 1
        page_size = -40

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )
        assert response.status == 422

    async def test_select_page_more_than_exists(self, make_get_request, setUp):
        query_data = "Test film"
        page_number = 20
        page_size = 20
        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == 404

    async def test_validate_page_number(self, make_get_request, setUp):
        query_data = "Test film"
        page_number = "hello"
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )
        assert response.status == 422