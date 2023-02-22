import random
from dataclasses import asdict

from loguru import logger

from common.models import WatchLater
from common.fakedata import fakeids


def random_user_watch_later(user_id: str) -> WatchLater:
    return WatchLater(
        user_id=user_id,
        films=[random.choice(fakeids.films_id) for _ in range(33)]
    )


def fake_user_watch_later_data() -> dict[str, list[str, ]]:
    """Генератор случайных записей."""
    for user_id in fakeids.users_id:
        yield asdict(random_user_watch_later(user_id))


async def insert_fake_user_watch_later_data(collection):
    """Запись данных в MongoDB."""
    await collection.delete_many({})
    await collection.insert_many([watch_later for watch_later in fake_user_watch_later_data()])
    count_docs = await collection.count_documents({})
    logger.info(f'inserted {count_docs} docs to collection.')
