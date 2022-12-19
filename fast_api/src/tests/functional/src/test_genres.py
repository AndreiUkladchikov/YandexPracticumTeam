import pytest

from tests.functional.models.models import Genre
from tests.functional.testdata.data_genres import test_genres


@pytest.mark.asyncio
class TestGenre:
    async def test_genres(self, set_up_genres, make_get_request):
        response = await make_get_request("genres")
        assert response.status == 200
        genres = [Genre(**genre) for genre in test_genres]
        assert genres == response.body["genres"]

    async def test_current_genre(self, set_up_genres, make_get_request):
        genre = Genre(**test_genres[0])
        response = await make_get_request(f"genres/{genre.id}")
        assert response.status == 200 and genre == response.body
