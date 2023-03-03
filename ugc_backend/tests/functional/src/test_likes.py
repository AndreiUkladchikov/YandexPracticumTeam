from http import HTTPStatus

payload = {"user_id": "test_user", "film_id": "test_film"}

rating = {"rating": 10}

payload_with_rating = {**payload, **rating}

film = {"film_id": "test_film"}
user2 = {"user_id": "test_user_2"}

common_url = "/api/v1/likes"


class TestLike:
    def test_like_by_film_id(self, client, delete_likes_collection):
        client.post(common_url + "/add_rating", params=payload_with_rating)
        response = client.get(common_url, params=film)
        assert response.status_code == HTTPStatus.OK

    def test_delete_like(self, client, delete_likes_collection):
        client.post(common_url + "/add_rating", params=payload_with_rating)
        response = client.delete(common_url + "/delete_rating", params=payload)
        assert response.status_code == HTTPStatus.OK

    def test_average_rating(self, client, delete_likes_collection):
        client.post(common_url + "/add_rating", params=payload_with_rating)
        response = client.get(common_url + "/rating", params=film)
        assert response.status_code == HTTPStatus.OK
