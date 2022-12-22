import pytest
import http
from functional.config import test_settings
from functional.models.models import Genre
from functional.testdata.data_genres import test_genres
from functional.utils.helpers import make_get_request


@pytest.mark.asyncio
async def test_cache_current_genre(es_delete_data, es_write_data):
    await es_write_data(test_genres, test_settings.genre_index)
    genre = Genre(**test_genres[0])
    await make_get_request(f"genres/{genre.id}")
    await es_delete_data(test_settings.genre_index)
    response = await make_get_request(f"genres/{genre.id}")

    assert response.status == http.HTTPStatus.OK and genre == response.body


@pytest.mark.asyncio
class TestGenre:
    async def test_genres(self, set_up_genres):
        response = await make_get_request("genres")
        assert response.status == http.HTTPStatus.OK
        genres = [Genre(**genre) for genre in test_genres]
        assert genres[0] == response.body["genres"][0]

    async def test_genres_validate_page_size(self, set_up_persons):
        page_number = 1
        page_size = -40

        response = await make_get_request(
            "genres", page_number=page_number, page_size=page_size
        )
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_genres_validate_page_number(self, set_up_genres):
        page_number = "test"
        page_size = 20

        response = await make_get_request(
            "genres", page_number=page_number, page_size=page_size
        )
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_genres_page_more_than_exists(self, set_up_genres):
        page_number = 20
        page_size = 20
        response = await make_get_request(
            "genres", page_number=page_number, page_size=page_size
        )
        assert response.status == http.HTTPStatus.NOT_FOUND

    async def test_current_genre(self, set_up_genres):
        genre = Genre(**test_genres[0])
        response = await make_get_request(f"genres/{genre.id}")
        assert response.status == http.HTTPStatus.OK and genre == response.body

    async def test_genre_doesnt_exist(self, set_up_genres):
        genre_id = "doesnt_exist"
        response = await make_get_request(end_of_url=f"genres/{genre_id}")
        assert response.status == http.HTTPStatus.NOT_FOUND
