import http

import pytest
from functional.config import test_settings
from functional.models.models import Film
from functional.testdata.data_main_page import (
    cache_films_main_page,
    test_films_main_page,
)
from functional.utils.helpers import make_get_request


@pytest.mark.asyncio
async def test_cache(es_delete_data, es_write_data):
    await es_write_data(test_films_main_page, test_settings.movie_index)
    await es_write_data(cache_films_main_page, test_settings.movie_index)

    response = await make_get_request("films")
    first_response = response.body
    assert response.status == http.HTTPStatus.OK

    # Delete 1 film from elastic
    await es_delete_data(test_settings.movie_index)

    response = await make_get_request("films")

    assert response.status == http.HTTPStatus.OK

    assert first_response == response.body


@pytest.mark.asyncio
class TestMainPage:
    async def test_without_parameters(self, set_up_main_page):
        response = await make_get_request("films")
        assert response.status == http.HTTPStatus.OK
        films = [Film(**film) for film in test_films_main_page]

        # Сравниваем вызов без параметров
        # Первым будет наш тестовый фильм с нереальным рейтингом 99.9
        assert films[0] == response.body["films"][0]

    async def test_imdb_rating(self, set_up_main_page):
        response = await make_get_request("films", sort="imdb_rating")
        assert response.status == http.HTTPStatus.OK
        assert (
            response.body["films"][0]["imdb_rating"]
            <= response.body["films"][1]["imdb_rating"]
        )

    async def test_desc_imdb_rating(self, set_up_main_page):
        response = await make_get_request("films", sort="-imdb_rating")
        assert response.status == http.HTTPStatus.OK
        assert (
            response.body["films"][0]["imdb_rating"]
            >= response.body["films"][1]["imdb_rating"]
        )

    async def test_genre_sort(self, set_up_main_page):
        response = await make_get_request(
            "films", genre="3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"
        )
        assert response.status == http.HTTPStatus.OK
        assert response.body["films"][0]["title"] == "First film"

    async def test_invalid_genre(self, set_up_main_page):
        response = await make_get_request("films", genre="1234")
        assert response.status == http.HTTPStatus.NOT_FOUND
