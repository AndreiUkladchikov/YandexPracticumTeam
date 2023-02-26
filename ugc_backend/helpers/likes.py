from models.db_models import AboutFilm
from models.likes import Likes, Rating


def average(doc: dict) -> float:
    if doc:
        film = AboutFilm(**doc)
        up = film.likes.up.count
        down = film.likes.down.count
        return (int(Rating.up) * up + int(Rating.down) * down) / (up + down)


def delete_like(doc: dict, user_id: str):
    if doc:
        film = AboutFilm(**doc)
        if user_id in film.likes.up.ids:
            film.likes.up.ids.remove(user_id)
            film.likes.up.count -= 1
        elif user_id in film.likes.down.ids:
            film.likes.down.ids.remove(user_id)
            film.likes.down.count -= 1

        return film.likes.dict()


def add_like(doc: dict, user_id: str) -> dict:
    if doc:
        film = AboutFilm(**doc)
        if user_id not in film.likes.up.ids:
            film.likes.up.ids.append(user_id)
            film.likes.up.count += 1

        if user_id in film.likes.down.ids:
            film.likes.down.ids.remove(user_id)
            film.likes.down.count -= 1
        result_likes = film.likes.dict()

    else:
        user_like = Likes(**{"up": {"count": 1, "ids": [user_id]}})
        result_likes = user_like.dict()
    return result_likes


def add_dislike(doc: dict, user_id: str):
    if doc:
        film = AboutFilm(**doc)
        if user_id not in film.likes.down.ids:
            film.likes.down.ids.append(user_id)
            film.likes.down.count += 1

        if user_id in film.likes.up.ids:
            film.likes.up.ids.remove(user_id)
            film.likes.up.count -= 1
        result_dislikes = film.likes.dict()

    else:
        user_like = Likes(**{"down": {"count": 1, "ids": [user_id]}})

        result_dislikes = user_like.dict()
    return result_dislikes
