import pytest
from core.config import settings
from fastapi.testclient import TestClient
from main import app
from pymongo import MongoClient


@pytest.fixture(scope="session")
def prepare_db():
    client = MongoClient(host=settings.mongo)
    db = client[settings.mongo_db]
    yield db


@pytest.fixture(scope="function")
def delete_bookmark_collection(bookmark_collection):
    bookmark_collection.delete_many({})
    yield
    bookmark_collection.delete_many({})


@pytest.fixture(scope="function")
def delete_review_collection(review_collection):
    review_collection.delete_many({})
    yield
    review_collection.delete_many({})


@pytest.fixture(scope="function")
def delete_likes_collection(likes_collection):
    likes_collection.delete_many({})
    yield
    likes_collection.delete_many({})


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="class")
def bookmark_collection(prepare_db):
    yield prepare_db.get_collection(settings.bookmarks_collection)


@pytest.fixture(scope="class")
def review_collection(prepare_db):
    yield prepare_db.get_collection(settings.reviews_collection)


@pytest.fixture(scope="class")
def likes_collection(prepare_db):
    yield prepare_db.get_collection(settings.like_collection)
