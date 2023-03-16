from typing import Any
from uuid import uuid4

import pytest
from tests.config import settings


@pytest.fixture
def user_id() -> str:
    return settings.test_user_id


@pytest.fixture
def user_expected() -> dict[str, Any]:
    return {
        "email": "testuser@test.loc",
        "firstname": "John",
    }


@pytest.fixture
def film_id() -> str:
    return settings.test_film_id


@pytest.fixture
def film_expected() -> dict[str, Any]:
    return {"title": "Star Wars Episode XXX", "rating": 9.9}


@pytest.fixture
def template() -> str:
    return r"""{{ user.get('firstname') }}, ваш отзыв к фильму {{ film.get('title') }} понравился пользователю!"""


@pytest.fixture
def context(user_id: str, film_id: str) -> dict[str, Any]:
    from worker.message_render import MessagePreRender
    
    return {"user": MessagePreRender.get_user_info(user_id), "film": MessagePreRender.get_film_info(film_id)}


@pytest.fixture
def message_expected(user_expected: dict[str, Any], film_expected: dict[str, Any]) -> str:
    return f"{user_expected.get('firstname')}, ваш отзыв к фильму {film_expected.get('title')} понравился пользователю!"
