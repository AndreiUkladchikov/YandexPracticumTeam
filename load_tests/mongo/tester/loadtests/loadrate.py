import random

from common.asynctimer import timeit
from common.fakedata import fakeids


@timeit
async def get_film_likes_and_dislikes(collection,
                                      film_id: str = random.choice(fakeids.films_id)) -> None:
    """Количество лайков и дизлайков у определённого фильма."""
    _query = {'film_id': {'$eq': film_id}}
    _fields = {'film_id': 1,
               'likes.up.count': 1,
               'likes.down.count': 1}
    _ = await collection.find_one(_query, _fields)


@timeit
async def get_film_avg_review_rate(collection,
                                   film_id: str = random.choice(fakeids.films_id)) -> None:
    """Средняя пользовательская оценка фильма."""
    _pipeline = [
        {'$unwind': '$reviews'},
        {'$group':
            {
                '_id': '$film_id',
                'avg_rate': {'$avg': '$reviews.mark'}
            }
         },
        {'$addFields':
            {
                'avg_rate': {'$round': ['$avg_rate', 3]}
            }
         },
        {'$match':
            {
                '_id': {'$eq': film_id}
            }
         }
    ]
    cursor = collection.aggregate(_pipeline)
    _ = await cursor.to_list(length=None)


@timeit
async def user_like_film(collection,
                         film_id: str = random.choice(fakeids.films_id),
                         user_id: str = random.choice(fakeids.users_id)) -> None:
    """Добавление лайка."""
    doc = await collection.find_one({'film_id': {'$eq': film_id}})
    if user_id not in doc['likes']['up']['ids']:
        doc['likes']['up']['ids'].append(user_id)
        doc['likes']['up']['count'] += 1
    if user_id in doc['likes']['down']['ids']:
        doc['likes']['down']['ids'].remove(user_id)
        doc['likes']['down']['count'] -= 1
    _ = await collection.update_one({'film_id': doc['film_id']},
                                    {'$set': {'likes': doc['likes']}})


@timeit
async def user_unlike_film(collection) -> None:
    """Добавление дизлайка."""
    user_id = random.choice(fakeids.users_id)
    doc = await collection.find_one({'film_id': {'$eq': random.choice(fakeids.films_id)}})
    if user_id not in doc['likes']['down']['ids']:
        doc['likes']['down']['ids'].append(user_id)
        doc['likes']['down']['count'] += 1
    if user_id in doc['likes']['up']['ids']:
        doc['likes']['up']['ids'].remove(user_id)
        doc['likes']['up']['count'] -= 1
    _ = await collection.update_one({'film_id': doc['film_id']},
                                    {'$set': {'likes': doc['likes']}})


@timeit
async def user_loved_films(collection) -> None:
    """Cписок понравившихся пользователю фильмов (список лайков пользователя)."""
    user_id = random.choice(fakeids.users_id)
    cursor = collection.find({'likes.up.ids': {'$in': [user_id]}}, {'film_id': 1})
    _ = await cursor.to_list(length=None)


def run_query_test_for_rate(loop, collection) -> None:
    """Тестируем время выполнения запросов к MongoDB."""
    loop.run_until_complete(get_film_likes_and_dislikes(collection))
    loop.run_until_complete(get_film_avg_review_rate(collection))
    loop.run_until_complete(user_like_film(collection))
    loop.run_until_complete(user_unlike_film(collection))
    loop.run_until_complete(user_loved_films(collection))
