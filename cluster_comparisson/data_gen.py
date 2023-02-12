import json
import uuid
import random
from model import MovieWatch


def generate_range_data(range: int, as_tuple: bool):
    data = []
    count = 0
    while count < range:
        if as_tuple:
            value = (
                str(uuid.uuid1()),
                str(uuid.uuid1()),
                random.randint(100000, 1000000000)
            )
        else:
            movie = MovieWatch(
                str(uuid.uuid1()),
                str(uuid.uuid1()),
                random.randint(100000, 1000000000)
            )
            value = movie.__dict__
        data.append(value)
        count = count + 1
    return data
