from http import HTTPStatus

from db_models import User

from test_data import (
    user_credits,
    fake_user_credits,
    url_login,
    url_registration,
    url_check,
    url_logout,
    url_refresh_tokens,
)


# TODO: tests depend on each other
class TestRegistration:
    def test_valid_user(self, client):
        response_registration = client.post(url_registration, json=user_credits)

        assert response_registration.status_code == HTTPStatus.OK

        assert (
            User.query.filter_by(email=user_credits.get("email")).one_or_none()
            is not None
        )

    def test_repeated_registration(self, client):
        response_registration = client.post(url_registration, json=user_credits)
        assert response_registration.status_code == HTTPStatus.UNAUTHORIZED

    def test_invalid_credentials(self, client):
        response_registration = client.post(
            url_registration, json={"email": 123, "password": 123}
        )

        assert response_registration.status_code == HTTPStatus.BAD_REQUEST


class TestLogin:
    def test_without_params(self, client):
        response = client.post(url_login, json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_fake_credits(self, client):
        response = client.post(url_login, json=fake_user_credits)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_valid_user(self, client):
        client.post(url_registration, json=user_credits)

        response_login = client.post(url_login, json=user_credits)

        assert response_login.status_code == HTTPStatus.OK

        is_access_token_in_payload = "access_token" in response_login.json
        assert is_access_token_in_payload is True

        is_refresh_token_in_payload = "refresh_token" in response_login.json
        assert is_refresh_token_in_payload is True


class TestJWTAccessToken:
    def test_login_with_access_token(self, create_user):
        client = create_user.get("client")
        access_token = create_user.get("access_token")
        refresh_token = create_user.get("refresh_token")
        hed = {"Authorization": "Bearer " + access_token}

        response = client.post(url_check, headers=hed)

        assert response.status_code == HTTPStatus.OK

        assert response.json["logged_in_as"] == user_credits["email"]


class TestLogout:
    def test_logout(self, create_user):
        client = create_user.get("client")
        access_token = create_user.get("access_token")
        hed = {"Authorization": "Bearer " + access_token}

        response = client.post(url_logout, headers=hed)

        assert response.status_code == HTTPStatus.OK

        response = client.post(url_logout, headers=hed)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

        assert (
            User.query.filter_by(
                email=user_credits.get("refresh_password")
            ).one_or_none()
            is None
        )


class TestRefreshTokens:
    def test_refresh(self, create_user):
        client = create_user.get("client")
        refresh_token = create_user.get("refresh_token")

        hed = {"Authorization": "Bearer " + refresh_token}

        response_refresh = client.post(url_refresh_tokens, headers=hed)

        assert response_refresh.status_code == HTTPStatus.OK

        is_access_token_in_payload = "access_token" in response_refresh.json
        assert is_access_token_in_payload is True

        is_refresh_token_in_payload = "refresh_token" in response_refresh.json
        assert is_refresh_token_in_payload is True

    def test_with_old_token(self, create_user):
        client = create_user.get("client")
        refresh_token = create_user.get("refresh_token")

        hed = {"Authorization": "Bearer " + refresh_token}

        client.post(url_refresh_tokens, headers=hed)

        response_with_old_token = client.post(url_refresh_tokens, headers=hed)
        assert response_with_old_token.status_code == HTTPStatus.UNAUTHORIZED

    def test_without_params(self, client):
        response = client.post(url_login, json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST
