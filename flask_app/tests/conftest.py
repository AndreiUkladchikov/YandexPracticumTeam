import pytest
from test_data import url_login, url_registration, user_credits

from clients import HttpClient, postgres_client
from db_models import User
from services import AccessHistoryService, CustomService

user_service = CustomService(client=postgres_client, model=User)
access_history_service = AccessHistoryService(postgres_client)


@pytest.fixture(scope="class")
def http_session():
    with HttpClient().get_session() as session:
        yield session
    access_history_service.clear()
    user_service.clear()


@pytest.fixture
def create_user(http_session) -> dict:
    http_session.post(url_registration, json=user_credits)
    response_login = http_session.post(url_login, json=user_credits)
    access_token: str = response_login.json().get("access_token")
    refresh_token: str = response_login.json().get("refresh_token")

    yield {
        "http_session": http_session,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
