from http import HTTPStatus

from test_data import url_check, url_login, url_registration, user_credits

from clients import postgres_client
from services import UserService

user_service = UserService(postgres_client)


# TODO: tests depend on each other
class TestRegistration:
    def test_valid_user(self, http_session):
        response_registration = http_session.post(url_registration, json=user_credits)

        assert response_registration.status_code == HTTPStatus.OK
        assert user_service.get({"email": user_credits.get("email")}) is not None

    def test_repeated_registration(self, http_session):
        response_registration = http_session.post(url_registration, json=user_credits)
        assert response_registration.status_code == HTTPStatus.UNAUTHORIZED

    def test_invalid_credentials(self, http_session):
        response_registration = http_session.post(
            url_registration, json={"email": 123, "password": 123}
        )
        assert response_registration.status_code == HTTPStatus.BAD_REQUEST


class TestLogin:
    def test_without_params(self, http_session):
        response = http_session.post(url_login, json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_fake_credits(self, http_session):
        response = http_session.post(
            url_login, json={"email": "fake@user.ru", "password": "fake_password"}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_valid_user(self, http_session):
        http_session.post(url_registration, json=user_credits)

        response_login = http_session.post(url_login, json=user_credits)

        assert response_login.status_code == HTTPStatus.OK

        is_access_token_in_payload = "access_token" in response_login.json().keys()
        assert is_access_token_in_payload is True


class TestJWTAccessToken:
    def test_login_with_access_token(self, create_user):
        client = create_user[0]
        token = create_user[1]
        hed = {"Authorization": "Bearer " + token}

        response = client.post(url_check, headers=hed)

        assert response.status_code == 200

        assert response.json().get("logged_in_as") == user_credits["email"]
