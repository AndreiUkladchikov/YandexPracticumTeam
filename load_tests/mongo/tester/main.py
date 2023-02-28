import motor.motor_asyncio

from common.config import settings
from loadfakedata.fakerate import insert_fake_film_rate_data
from loadfakedata.fakewatchlater import insert_fake_user_watch_later_data
from loadtests.loadrate import run_query_test_for_rate
from loadtests.loadwatch import run_query_test_for_watch_later


def start_load_test() -> None:
    """Подключаемся к шарду MongoDB и тестируем время выполнения запросов."""
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_url)

    db_rate = client[settings.mongo_db_name]
    collection_rate = db_rate[settings.mongo_collection_rate]
    collection_watch = db_rate[settings.mongo_collection_watch]

    loop = client.get_io_loop()

    # Наполняем MongoDB
    loop.run_until_complete(insert_fake_film_rate_data(collection_rate))
    loop.run_until_complete(insert_fake_user_watch_later_data(collection_watch))
    # Тестируем время выполнения запросов к MongoDB
    run_query_test_for_rate(loop, collection_rate)
    run_query_test_for_watch_later(loop, collection_watch)


if __name__ == '__main__':
    start_load_test()
