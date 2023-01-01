import pytest

from app import app
from db import db
from db_models import User

user_credits: dict = {"email": "bali@mail.ru", "password": "bali123"}
url_login: str = "/api/v1/auth/login"
url_registration: str = "/api/v1/auth/registration"


@pytest.fixture(scope="class")
def client():
    with app.test_client() as client:
        yield client

    User.query.delete()
    db.session.commit()


@pytest.fixture
def database():
    yield User


@pytest.fixture()
def runner():
    return app.test_cli_runner()


@pytest.fixture
def create_user(client):
    client.post(url_registration, json=user_credits)
    response_login = client.post(url_login, json=user_credits)
    access_token: str = response_login.json["access_token"]

    yield client, access_token
