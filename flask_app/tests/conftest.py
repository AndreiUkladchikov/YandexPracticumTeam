import pytest
from db import db
from test_data import url_login, url_registration, user_credits

from app import app
from db_models import User


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
