from __future__ import annotations

import pytest

from pydantic import BaseModel
from config import test_settings
from testdata.data_main_page import test_main_page_genres, test_films_main_page, cache_films_main_page

pytestmark = pytest.mark.asyncio


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float | None


@pytest.mark.asyncio
async def test_cache(make_get_request, es_delete_data, es_write_data):
    await es_write_data(test_films_main_page, test_settings.movie_index)
    await es_write_data(cache_films_main_page, test_settings.movie_index)

    response = await make_get_request("films")
    firstResponse = response.body
    assert response.status == 200

    # Delete 1 film from elastic
    await es_delete_data(test_settings.movie_index, 'a38e738e-ac45-40ff-9f98-ab7a0ff45054')

    response = await make_get_request("films")

    assert response.status == 200

    assert firstResponse == response.body


@pytest.mark.asyncio
class TestMainPage:
    async def test_without_parameters(self, make_get_request, set_up_main_page):
        response = await make_get_request("films")
        assert response.status == 200
        films = [Film(**film) for film in test_films_main_page]

        # Сравниваем вызов без параметров
        # Первым будет наш тестовый фильм с нереальным рейтингом 99.9
        assert films[0] == response.body['films'][0]

    async def test_imdb_rating(self, make_get_request, set_up_main_page):
        response = await make_get_request("films", sort="imdb_rating")
        assert response.status == 200
        assert response.body['films'][0]['imdb_rating'] <= response.body['films'][1]['imdb_rating']

    async def test_desc_imdb_rating(self, make_get_request, set_up_main_page):
        response = await make_get_request("films", sort="-imdb_rating")
        assert response.status == 200
        assert response.body['films'][0]['imdb_rating'] >= response.body['films'][1]['imdb_rating']

    async def test_genre_sort(self, make_get_request, set_up_main_page):
        response = await make_get_request("films", genre="3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff")
        assert response.status == 200
        assert response.body['films'][0]['title'] == 'First film'

    async def test_invalid_genre(self, make_get_request, set_up_main_page):
        response = await make_get_request("films", genre="1234")
        assert response.status == 404
