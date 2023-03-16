from typing import Any

from worker.message_render import MessagePreRender


def test_get_user_info(user_id: str, user_expected: dict[str, Any]) -> None:
    user = MessagePreRender.get_user_info(user_id)
    assert user.get("firstname") == user_expected.get("firstname"), "User firstname not equal to expected"
    assert user.get("email") == user_expected.get("email"), "User email not equal to expected"


def test_get_film_info(film_id: str, film_expected: dict[str, Any]) -> None:
    film = MessagePreRender.get_film_info(film_id)
    assert film.get("title") == film_expected.get("title"), "Film title not equal to expected"
    assert film.get("rating") == film_expected.get("rating"), "Film rating not equal to expected"


def test_render_template(template: str, context: dict[str, Any], message_expected: str) -> None:
    message = MessagePreRender.render_template(template, context)
    assert message == message_expected, "Rendered message not equal to expected"
