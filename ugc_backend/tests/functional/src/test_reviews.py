from http import HTTPStatus

film = {"film_id": "test_film"}
user = {"user_id": "test_user"}

film_user = {**user, **film}

film_user_text = {**film_user, "text": "Perfect film"}

film_user_text_rating = {**film_user_text, "rating": "10"}

rating = {"rating": "1"}
sort = {"sort": "likes"}

film_user_rating = {**film_user, **rating}


common_url = "/api/v1/reviews"


class TestReview:
    def test_show_all_reviews_of_film(self, client, delete_review_collection):
        client.post(common_url + "/add_review", params=film_user_text_rating)
        response = client.get(common_url, params=film)
        assert response.status_code == HTTPStatus.OK

    def test_add_like_to_review(self, client, delete_review_collection):
        resp = client.post(common_url + "/add_review", params=film_user_text_rating)
        review_id = resp.json()
        response = client.post(
            common_url + "/add_like", params={**film_user_rating, **review_id}
        )
        assert response.status_code == HTTPStatus.OK

    def test_asc_sort_like(self, client, delete_review_collection):
        client.post(common_url + "/add_review", params=film_user_text_rating)
        response = client.get(common_url, params={**film, **sort})
        assert response.status_code == HTTPStatus.OK

    def test_non_existent_film_id(self, client, delete_review_collection):
        response = client.get(common_url, params=film)
        assert response.status_code == HTTPStatus.NOT_FOUND
