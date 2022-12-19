import pytest

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором
#  `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
class TestSearch:
    async def test_search(self, make_get_request, set_up_search_films):
        query_data = "First film"

        response = await make_get_request("films/search", query_data)

        assert response.status == 200
        assert response.body[0]["title"] == query_data

    async def test_search_paging_first_page(self, make_get_request, set_up_search_films):
        query_data = "First film"
        page_number = 1
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == 200
        assert len(response.body) == page_size

    async def test_search_paging_last_page(self, make_get_request, set_up_search_films):
        query_data = "First film"
        page_number = 3
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == 200
        assert len(response.body) == page_size

    async def test_validate_page_size(self, make_get_request, set_up_search_films):
        query_data = "Test film"
        page_number = 1
        page_size = -40

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )
        assert response.status == 422

    async def test_select_page_more_than_exists(self, make_get_request, set_up_search_films):
        # Граничное условие. Тестируем 100 страницу
        query_data = "Test film"
        page_number = 100
        page_size = 20
        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )

        assert response.status == 404

    async def test_validate_page_number(self, make_get_request, set_up_search_films):
        query_data = "Test film"
        page_number = "hello"
        page_size = 20

        response = await make_get_request(
            "films/search", query_data, page_number=page_number, page_size=page_size
        )
        assert response.status == 422
