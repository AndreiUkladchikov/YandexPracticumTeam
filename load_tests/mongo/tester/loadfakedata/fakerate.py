import random
import string
import time
from dataclasses import asdict
from datetime import datetime
from uuid import uuid4, UUID

from loguru import logger

from common.config import settings
from common.models import Up, Down, Likes, ReviewEvaluation, Review, FilmUserRate
from common.fakedata import fakeids


def random_up() -> Up:
    up_votes = [fakeids.users_id[i] for i in range(random.randint(10, settings.max_up_votes_count))]
    return Up(ids=up_votes, count=len(up_votes))


def random_down() -> Down:
    down_votes = [fakeids.users_id[i] for i in range(random.randint(10, settings.max_down_votes_count))]
    return Down(ids=down_votes, count=len(down_votes))


def random_likes() -> Likes:
    return Likes(up=random_up(), down=random_down())


def random_review_evaluation() -> ReviewEvaluation:
    return ReviewEvaluation(up=random_up(), down=random_down())


def random_review() -> Review:
    return Review(
        id=str(uuid4()),
        user_id=random.choice(fakeids.users_id),
        firstname=''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))),
        lastname=''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))),
        created=datetime.now(),
        mark=random.randint(1, 10),
        text=''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(15, 150))),
        review_evaluation=random_review_evaluation()
    )


def random_film_user_rate(film_id: str) -> FilmUserRate:
    return FilmUserRate(
        film_id=film_id,
        reviews=[random_review() for _ in range(random.randint(10, settings.max_fake_reviews_count))],
        likes=random_likes()
    )


def fake_film_rate_data() -> dict[str, UUID | list[Review, ] | Likes]:
    """Генератор случайных записей."""
    for film_id in fakeids.films_id:
        yield asdict(random_film_user_rate(film_id))


async def insert_fake_film_rate_data(collection) -> None:
    """Запись данных в MongoDB."""
    await collection.delete_many({})
    _results = []
    for film_rate in fake_film_rate_data():
        start = time.time()
        _ = await insert_fake_film_rate_data_row(collection, film_rate)
        _results.append(time.time() - start)
    logger.info(
        f'Write FilmRateDoc results: max: {max(_results)}, min: {min(_results)}, avg: {sum(_results)/len(_results)}'
    )


async def insert_fake_film_rate_data_row(collection, film_rate) -> dict:
    """Записываем строку в MongoDB."""
    return await collection.insert_one(film_rate)
