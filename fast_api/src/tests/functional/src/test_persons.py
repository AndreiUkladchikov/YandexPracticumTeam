import pytest
from models.models import Film
from config import test_settings
from testdata.data_persons import (test_film_by_person, test_persons)


@pytest.mark.asyncio
class TestPerson:
    async def test_search_person(self, set_up_persons, make_get_request):
        person_name = test_persons[0]["full_name"]
        response = await make_get_request(
            end_of_url="persons/search",
            query=person_name
        )
        assert response.status == 200
        person_id = test_persons[0]["id"]
        assert person_id == response.body[0]["id"] and person_name == response.body[0]["full_name"]

    async def test_search_person_validate_page_size(self, set_up_persons, make_get_request):
        person_name = test_persons[0]["full_name"]
        page_number = 1
        page_size = -40

        response = await make_get_request(
            "persons/search", person_name, page_number=page_number, page_size=page_size
        )
        assert response.status == 422

    async def test_search_person_validate_page_number(self, set_up_persons, make_get_request):
        person_name = test_persons[0]["full_name"]
        page_number = "test"
        page_size = 20

        response = await make_get_request(
            "persons/search", person_name, page_number=page_number, page_size=page_size
        )
        assert response.status == 422

    async def test_search_person_page_more_than_exists(
            self, set_up_persons, make_get_request
    ):
        person_name = test_persons[0]["full_name"]
        page_number = 20
        page_size = 20
        response = await make_get_request(
            "persons/search", person_name, page_number=page_number, page_size=page_size
        )

        assert response.status == 404

    async def test_current_person(self, set_up_persons, make_get_request):
        person_id = test_persons[1]["id"]
        response = await make_get_request(
            end_of_url=f"persons/{person_id}"
        )
        assert response.status == 200
        person_name = test_persons[1]["full_name"]
        person_film = test_persons[1]["writer_in"]
        assert person_name == response.body["full_name"] and person_film == response.body["film_ids"]

    async def test_person_doesnt_exist(self, set_up_persons, make_get_request):
        person_id = "doesnt_exist"
        response = await make_get_request(
            end_of_url=f"persons/{person_id}"
        )
        assert response.status == 404

    async def test_film_by_person(self, set_up_persons, make_get_request):
        person_id = test_persons[2]["id"]
        response = await make_get_request(
            end_of_url=f"persons/{person_id}/film"
        )
        assert response.status == 200
        film = Film(**test_film_by_person[0])
        assert film == response.body["films"][0]

    async def test_search_cached_current_person(self, set_up_persons, make_get_request, es_delete_data):
        person_id = test_persons[1]["id"]
        await es_delete_data(test_settings.person_index)
        response = await make_get_request(
            end_of_url=f"persons/{person_id}"
        )
        assert response.status == 200
        person_name = test_persons[1]["full_name"]
        person_film = test_persons[1]["writer_in"]
        assert person_name == response.body["full_name"] and person_film == response.body["film_ids"]