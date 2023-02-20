import random

from asynctimer import timeit
from fakedata import RANDOM_FILM_ID


@timeit
async def get_film_user_rate(collection):
    _ = await collection.find_one({'film_id': {'$eq': random.choice(RANDOM_FILM_ID)}})
