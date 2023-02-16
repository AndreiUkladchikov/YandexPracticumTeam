#!/usr/bin/python3

import motor.motor_asyncio


CONNECTION_URL = 'mongodb://127.0.0.1:27019,127.0.0.1:27020'
DB_NAME = 'someTestDb'
COLLECTION_NAME = 'testCollection'


client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def fake_data(count: int = 1000):
    """Генератор случайных записей."""
    for i in range(count):
        yield {'i': i}


async def do_insert():
    """Запись данных в MongoDB."""
    result = await db.test_collection.insert_many(
        [i for i in fake_data(2000)])
    print(f'inserted {len(result.inserted_ids)} docs')


if __name__ == '__main__':
    loop = client.get_io_loop()
    loop.run_until_complete(do_insert())
