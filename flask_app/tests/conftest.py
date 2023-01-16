import pytest
from test_data import url_login, url_registration, user_credits

from clients import HttpClient, postgres_client
from services import UserService

user_service = UserService(postgres_client)


@pytest.fixture(scope="class")
def http_session():
    with HttpClient().get_session() as session:
        yield session
    user_service.clear()


@pytest.fixture
def create_user(http_session):
    http_session.post(url_registration, json=user_credits)
    response_login = http_session.post(url_login, json=user_credits)
    access_token: str = response_login.json().get("access_token")

    yield http_session, access_token
