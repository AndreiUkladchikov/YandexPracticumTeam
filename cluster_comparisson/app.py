# 1. Create tables in Clickhouse and Vertica
# 2. Start loop for 4 000 000 records:
# 2.1. Generate fake data
# 2.2. Save to Clickhouse and Vertica

import time

import constants
from clickhouse.client import count_rows as count_clickhouse
from clickhouse.client import insert_data as insert_to_clickhouse
from data_gen import generate_range_data
from loguru import logger
from storage_telemetry import save_telemetry
from vertica.client import count_rows as count_vertica
from vertica.client import insert_rows as insert_to_vertica

TOTAL_ROWS_AMOUNT = 4000000
BULK_CHUNK = 100


def fill_db():
    clickhouse_count = count_clickhouse()
    while clickhouse_count[0][0] < TOTAL_ROWS_AMOUNT:
        data = generate_range_data(BULK_CHUNK, False)
        insert_to_clickhouse(data)
        clickhouse_count = count_clickhouse()

    vertica_count = count_vertica()
    while vertica_count < TOTAL_ROWS_AMOUNT:
        data = generate_range_data(BULK_CHUNK, True)
        insert_to_clickhouse(data)
        vertica_count = count_vertica()


if __name__ == "__main__":
    fill_db()
