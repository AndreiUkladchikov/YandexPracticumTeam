import random

from common.asynctimer import timeit
from common.fakedata import fakeids


@timeit
async def get_user_watch_later_films(collection,
                                     user_id: str = random.choice(fakeids.users_id)) -> None:
    """Получаем список фильмов пользователя для просмотра позже."""
    _query = {'user_id': {'$eq': user_id}}
    _ = await collection.find_one(_query)


def run_query_test_for_watch_later(loop, collection) -> None:
    """Тестируем время выполнения запросов к MongoDB."""
    loop.run_until_complete(get_user_watch_later_films(collection))
