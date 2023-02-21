import random
import string
from dataclasses import asdict
from datetime import datetime
from uuid import uuid4, UUID

from loguru import logger

from models import Up, Down, Likes, ReviewEvaluation, Review, FilmUserRate


RANDOM_FILM_ID = [str(uuid4()) for _ in range(100)]
RANDOM_USER_ID = [str(uuid4()) for _ in range(100)]


def random_up() -> Up:
    up_votes = [RANDOM_USER_ID[i] for i in range(random.randint(10, 100))]
    return Up(ids=up_votes, count=len(up_votes))


def random_down() -> Down:
    down_votes = [RANDOM_USER_ID[i] for i in range(random.randint(10, 100))]
    return Down(ids=down_votes, count=len(down_votes))


def random_likes() -> Likes:
    return Likes(up=random_up(), down=random_down())


def random_review_evaluation() -> ReviewEvaluation:
    return ReviewEvaluation(up=random_up(), down=random_down())


def random_review() -> Review:
    return Review(
        id=str(uuid4()),
        user_id=random.choice(RANDOM_USER_ID),
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
        reviews=[random_review() for _ in range(random.randint(10, 100))],
        likes=random_likes()
    )


def fake_film_rate_data() -> dict[str, UUID | list[Review, ] | Likes]:
    """Генератор случайных записей."""
    for film_id in RANDOM_FILM_ID:
        yield asdict(random_film_user_rate(film_id))


async def insert_fake_data(collection):
    """Запись данных в MongoDB."""
    await collection.delete_many({})
    await collection.insert_many([film_rate for film_rate in fake_film_rate_data()])
    count_docs = await collection.count_documents({})
    logger.info(f'inserted {count_docs} docs to collection.')
