from __future__ import annotations

import pytest
from tests.functional.models.models import Film
from tests.functional.settings import test_settings
from tests.functional.testdata.data_main_page import test_films_main_page


@pytest.mark.asyncio
class TestMainPage:
    async def test_without_parameters(self, make_get_request, set_up_main_page):
        response = await make_get_request("films")
        assert response.status == 200
        films = [Film(**film) for film in test_films_main_page]

        assert films == response.body["films"]

    async def test_imdb_rating(self, make_get_request, set_up_main_page):
        response = await make_get_request("films", sort="imdb_rating")
        assert response.status == 200
        assert (
            response.body["films"][0]["imdb_rating"]
            <= response.body["films"][1]["imdb_rating"]
        )

    async def test_desc_imdb_rating(self, make_get_request, set_up_main_page):
        response = await make_get_request("films", sort="-imdb_rating")
        assert response.status == 200
        assert (
            response.body["films"][0]["imdb_rating"]
            >= response.body["films"][1]["imdb_rating"]
        )

    async def test_genre_sort(self, make_get_request, set_up_main_page):
        response = await make_get_request(
            "films", genre="3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"
        )
        assert response.status == 200
        assert response.body["films"][0]["title"] == "First film"

    async def test_invalid_genre(self, make_get_request, set_up_main_page):
        response = await make_get_request("films", genre="1234")
        assert response.status == 404


@pytest.mark.asyncio
async def test_cache(make_get_request, es_delete_data, es_write_data):
    await es_write_data(test_films_main_page, test_settings.movie_index)

    response = await make_get_request("films")
    assert response.status == 200

    await es_delete_data(test_settings.movie_index)

    response = await make_get_request("films")

    assert response.status == 200

    films = [Film(**film) for film in test_films_main_page]

    assert films == response.body["films"]
