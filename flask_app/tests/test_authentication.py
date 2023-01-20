from http import HTTPStatus

from test_data import (fake_user_credits, new_user_credits, url_change_credits,
                       url_login, url_login_history, url_logout,
                       url_refresh_tokens, url_registration, user_credits)

from clients import postgres_client
from db_models import User
from services import CustomService

user_service = CustomService(client=postgres_client, model=User)


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
        assert response_registration.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestLogin:
    def test_without_params(self, http_session):
        response = http_session.post(url_login, json={})
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_fake_credits(self, http_session):
        response = http_session.post(url_login, json=fake_user_credits)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_valid_user(self, http_session):
        http_session.post(url_registration, json=user_credits)

        response_login = http_session.post(url_login, json=user_credits)

        assert response_login.status_code == HTTPStatus.OK

        is_access_token_in_payload = "access_token" in response_login.json().keys()
        assert is_access_token_in_payload is True

        is_refresh_token_in_payload = "refresh_token" in response_login.json().keys()
        assert is_refresh_token_in_payload is True


class TestLogout:
    def test_logout(self, create_user):
        http_session = create_user.get("http_session")
        access_token = create_user.get("access_token")
        hed = {"Authorization": "Bearer " + access_token}

        response = http_session.post(url_logout, headers=hed)

        assert response.status_code == HTTPStatus.OK

        response = http_session.post(url_logout, headers=hed)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

        user = user_service.get({"email": user_credits.get("email")})

        assert user.refresh_token is None


class TestRefreshTokens:
    def test_refresh(self, create_user):
        http_session = create_user.get("http_session")
        refresh_token = create_user.get("refresh_token")

        hed = {"Authorization": "Bearer " + refresh_token}

        response_refresh = http_session.post(url_refresh_tokens, headers=hed)

        assert response_refresh.status_code == HTTPStatus.OK

        is_access_token_in_payload = "access_token" in response_refresh.json().keys()
        assert is_access_token_in_payload is True

        is_refresh_token_in_payload = "refresh_token" in response_refresh.json().keys()
        assert is_refresh_token_in_payload is True

    def test_with_old_token(self, create_user):
        http_session = create_user.get("http_session")
        refresh_token = create_user.get("refresh_token")

        hed = {"Authorization": "Bearer " + refresh_token}

        http_session.post(url_refresh_tokens, headers=hed)

        response_with_old_token = http_session.post(url_refresh_tokens, headers=hed)
        assert response_with_old_token.status_code == HTTPStatus.UNAUTHORIZED


class TestChangeCredits:
    def test_change_credits(self, create_user):
        http_session = create_user.get("http_session")
        access_token = create_user.get("access_token")

        hed = {"Authorization": "Bearer " + access_token}
        response = http_session.post(
            url_change_credits, json=new_user_credits, headers=hed
        )

        assert response.status_code == HTTPStatus.OK


class TestLoginHistory:
    def test_login_history(self, create_user):
        http_session = create_user.get("http_session")
        access_token = create_user.get("access_token")

        hed = {"Authorization": "Bearer " + access_token}
        response = http_session.get(url_login_history, headers=hed)
        assert response.status_code == HTTPStatus.OK
