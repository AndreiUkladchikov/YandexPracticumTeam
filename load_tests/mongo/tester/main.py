from uuid import uuid4

import motor.motor_asyncio

from fakedata import insert_fake_data
from loadtests import get_film_user_rate


CONNECTION_URL = 'mongodb://127.0.0.1:27019,127.0.0.1:27020'
DB_NAME = 'someTestDb'
COLLECTION_NAME = 'testCollection'


client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


if __name__ == '__main__':
    loop = client.get_io_loop()
    loop.run_until_complete(insert_fake_data(collection))
    loop.run_until_complete(get_film_user_rate(collection))
