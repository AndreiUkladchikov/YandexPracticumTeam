import random
import string
from dataclasses import asdict
from datetime import datetime
from uuid import uuid4, UUID

from loguru import logger

from models import Up, Down, Likes, ReviewEvaluation, Review, FilmUserRate
from fakedata import fakeids

max_up_votes_count = 100
max_down_votes_count = 100
max_fake_reviews_count = 100


def random_up() -> Up:
    up_votes = [fakeids.users_id[i] for i in range(random.randint(10, max_up_votes_count))]
    return Up(ids=up_votes, count=len(up_votes))


def random_down() -> Down:
    down_votes = [fakeids.users_id[i] for i in range(random.randint(10, max_down_votes_count))]
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
        reviews=[random_review() for _ in range(random.randint(10, max_fake_reviews_count))],
        likes=random_likes()
    )


def fake_film_rate_data() -> dict[str, UUID | list[Review, ] | Likes]:
    """Генератор случайных записей."""
    for film_id in fakeids.films_id:
        yield asdict(random_film_user_rate(film_id))
