import pytest

from app import app
from db import db
from db_models import User

from test_data import user_credits, url_login, url_registration


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
    refresh_token: str = response_login.json["refresh_token"]

    res = {"client": client, "access_token": access_token,
           "refresh_token": refresh_token}
    yield res
