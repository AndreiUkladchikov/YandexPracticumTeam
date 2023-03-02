from models.db_models import AboutFilm
from models.likes import Likes, Rating


def average(doc: dict) -> float:
    try:
        if doc and doc.get("likes"):
            film = AboutFilm(**doc)
            up = film.likes.up.count
            down = film.likes.down.count
            return (int(Rating.up) * up + int(Rating.down) * down) / (up + down)
    except ZeroDivisionError:
        return 0


def delete_like(doc: Likes, user_id: str):
    if doc:
        if user_id in doc.up.ids:
            doc.up.ids.remove(user_id)
            doc.up.count -= 1
        elif user_id in doc.down.ids:
            doc.down.ids.remove(user_id)
            doc.down.count -= 1

        return doc.dict()


def add_like(doc: Likes, user_id: str) -> Likes:
    if doc:
        if user_id not in doc.up.ids:
            doc.up.ids.append(user_id)
            doc.up.count += 1

        if user_id in doc.down.ids:
            doc.down.ids.remove(user_id)
            doc.down.count -= 1
        result_likes = doc

    else:
        user_like = Likes(**{"up": {"count": 1, "ids": [user_id]}})
        result_likes = user_like
    return result_likes


def add_dislike(doc: Likes, user_id: str) -> Likes:
    if doc:
        if user_id not in doc.down.ids:
            doc.down.ids.append(user_id)
            doc.down.count += 1

        if user_id in doc.up.ids:
            doc.up.ids.remove(user_id)
            doc.up.count -= 1
        result_dislikes = doc

    else:
        user_like = Likes(**{"down": {"count": 1, "ids": [user_id]}})
        result_dislikes = user_like
    return result_dislikes
