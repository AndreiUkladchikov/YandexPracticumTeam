# 1. Create tables in Clickhouse and Vertica
# 2. Start loop for 4 000 000 records:
# 2.1. Generate fake data
# 2.2. Save to Clickhouse and Vertica

import time

import constants
from clickhouse.client import insert_data as insert_to_clickhouse
from data_gen import generate_range_data
from loguru import logger
from storage_telemetry import save_telemetry
from vertica.client import insert_rows as insert_to_vertica

ITERATIONS = 10
BULK_CHUNK = 1000


def test_insert():
    ch_count = 0
    test_result = []
    while ch_count < ITERATIONS:
        speed = clickhouse_insert()
        test_result.append({"Operation": "Insert", "Rows": BULK_CHUNK, "Speed": speed})
        ch_count = ch_count + 1
        logger.info(f"Clickhouse {ch_count} test insert iterations")
    save_telemetry(constants.TYPE_INSERT, constants.CLICKHOUSE, BULK_CHUNK, test_result)

    ve_count = 0
    test_result = []
    while ve_count < ITERATIONS:
        speed = vertica_insert()
        test_result.append({"Operation": "Insert", "Rows": BULK_CHUNK, "Speed": speed})
        ve_count = ve_count + 1
        logger.info(f"Vertica {ve_count} test insert iterations")
    save_telemetry(constants.TYPE_INSERT, constants.VERTICA, BULK_CHUNK, test_result)


def clickhouse_insert():
    data = generate_range_data(BULK_CHUNK, False)
    # Меряем скорость записи
    start = time.perf_counter()
    insert_to_clickhouse(data)
    end = time.perf_counter()
    speed = (end - start) * 10**3
    return f"{speed:.03f} ms"


def vertica_insert():
    data = generate_range_data(BULK_CHUNK, True)
    # Меряем скорость записи
    start = time.perf_counter()
    insert_to_vertica(data)
    end = time.perf_counter()
    speed = (end - start) * 10**3
    return f"{speed:.03f} ms"


if __name__ == "__main__":
    test_insert()
