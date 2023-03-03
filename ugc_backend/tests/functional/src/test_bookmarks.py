from http import HTTPStatus

payload = {"user_id": "test_user", "film_id": "test_film"}

user = payload.copy()
user.pop("film_id")

common_url = "/api/v1/bookmarks"


class TestBookmark:
    def test_bookmark_by_user_id(self, client, delete_bookmark_collection):
        client.post(common_url + "/add_bookmark", params=payload)
        response = client.get(common_url, params=user)
        assert response.status_code == HTTPStatus.OK

    def test_delete_bookmark(self, client, delete_bookmark_collection):
        client.post(common_url + "/add_bookmark", params=payload)
        response = client.delete(common_url + "/delete_bookmark", params=payload)
        assert response.status_code == HTTPStatus.OK

    def test_user_has_no_bookmarks(self, client, delete_bookmark_collection):
        response = client.get(common_url, params=user)
        assert response.status_code == HTTPStatus.NOT_FOUND
