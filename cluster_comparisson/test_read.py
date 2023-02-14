# 1. Create tables in Clickhouse and Vertica
# 2. Start loop for 4 000 000 records:
# 2.1. Generate fake data
# 2.2. Save to Clickhouse and Vertica

import time

import constants
from clickhouse.client import read_rows as read_from_clickhouse
from loguru import logger
from storage_telemetry import save_telemetry
from vertica.client import read_rows as read_from_vertica

ITERATIONS = 50
BULK_CHUNK = 1000


def test_read():
    ch_count = 0
    test_result = []
    while ch_count < ITERATIONS:
        speed = clickhouse_read()
        test_result.append({"Operation": "Read", "Rows": "all", "Speed": speed})
        ch_count = ch_count + 1
        logger.info(f"Clickhouse {ch_count} test read iterations")
    save_telemetry(constants.TYPE_READ, constants.CLICKHOUSE, "", test_result)

    ve_count = 0
    test_result = []
    while ve_count < ITERATIONS:
        speed = vertica_read()
        test_result.append({"Operation": "Read", "Rows": "all", "Speed": speed})
        ve_count = ve_count + 1
        logger.info(f"Vertica {ve_count} test read iterations")
    save_telemetry(constants.TYPE_READ, constants.VERTICA, "", test_result)


def clickhouse_read():
    # Меряем скорость записи
    start = time.perf_counter()
    read_from_clickhouse()
    end = time.perf_counter()
    speed = (end - start) * 10**3
    return f"{speed:.03f} ms"


def vertica_read():
    # Меряем скорость записи
    start = time.perf_counter()
    read_from_vertica()
    end = time.perf_counter()
    speed = (end - start) * 10**3
    return f"{speed:.03f} ms"


if __name__ == "__main__":
    test_read()
