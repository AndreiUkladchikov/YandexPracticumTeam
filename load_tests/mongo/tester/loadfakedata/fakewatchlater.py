import random
import time
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


async def insert_fake_user_watch_later_data(collection) -> None:
    """Запись данных в MongoDB."""
    await collection.delete_many({})
    _results = []
    for watch_later in fake_user_watch_later_data():
        start = time.time()
        _ = await insert_fake_user_watch_later_data_row(collection, watch_later)
        _results.append(time.time() - start)
    logger.info(
        f'Write FilmWatchLaterDoc results: max: {max(_results)}, min: {min(_results)}, avg: {sum(_results)/len(_results)}'
    )


async def insert_fake_user_watch_later_data_row(collection, watch_later) -> dict:
    """Записываем строку в MongoDB."""
    return await collection.insert_one(watch_later)
