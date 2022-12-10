from uuid import uuid4
import pytest
from tests.functional.settings import test_settings

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором
#  `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.


@pytest.mark.asyncio
async def test_search(es_write_data, make_get_request, es_delete_data):
    # 1. Генерируем данные для ES

    es_data = [
        {
            "id": "111222333444",
            "type": "movie",
            "imdb_rating": 9.9,
            "genre": ["Action", "Sci-Fi"],
            "genres": [
                {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
                {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
            ],
            "title": "Baby nowhere",
            "description": "New World",
            "directors": [{"id": "123", "full_name": "Stan"}],
            "director": "Stan",
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [
                {"id": "111", "full_name": "Ann"},
                {"id": "222", "full_name": "Bob"},
            ],
            "writers": [
                {"id": "333", "full_name": "Ben"},
                {"id": "444", "full_name": "Howard"},
            ],
        }
        for _ in range(1)
    ]

    # 3. Запрашиваем данные из ES по API

    await es_write_data(es_data, test_settings.es_index)

    query_data = "Baby nowhere"

    # 4. Проверяем ответ
    response = await make_get_request("films/search", query_data)

    assert response.status == 200
    assert response.body[0]["title"] == query_data

    # 5. Зачищаем данные
    await es_delete_data(test_settings.es_index)


@pytest.mark.asyncio
async def test_search_paging(es_write_data, make_get_request, es_delete_data):
    # 1. Генерируем данные для ES

    es_data = [
        {
            "id": str(uuid4()),
            "type": "movie",
            "imdb_rating": 9.9,
            "genre": ["Action", "Sci-Fi"],
            "genres": [
                {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
                {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
            ],
            "title": "Baby nowhere",
            "description": "New World",
            "directors": [{"id": "123", "full_name": "Stan"}],
            "director": "Stan",
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [
                {"id": "111", "full_name": "Ann"},
                {"id": "222", "full_name": "Bob"},
            ],
            "writers": [
                {"id": "333", "full_name": "Ben"},
                {"id": "444", "full_name": "Howard"},
            ],
        }
        for _ in range(50)
    ]

    # 3. Запрашиваем данные из ES по API

    await es_write_data(es_data, test_settings.es_index)

    query_data = "Baby nowhere"

    # 4. Проверяем ответ
    response = await make_get_request("films/search", query_data, 1, 1)

    assert response.status == 200
    # assert response.body[0]["title"] == query_data

    # 5. Зачищаем данные
    await es_delete_data(test_settings.es_index)
