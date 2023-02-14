#!/usr/bin/env python3
from chloader.loader import ClickHouseLoader
from common.config import settings
from common.decorators import backoff
from datatransform.transform import DataTransform
from kafkaextract.extract import KafkaExtractor
from loguru import logger
from storage.storage import RedisStorage


@backoff()
def init_etl() -> None:

    extract = KafkaExtractor()
    loader = ClickHouseLoader(host=settings.clickhouse_host)
    storage = RedisStorage()

    loader.create_table()

    while True:
        read_count = settings.batch_size - storage.current_batch_size()
        for key, value in extract.extract_batch(read_count):
            storage.save(DataTransform.parse_kafka_data(key, value))
        batch = (DataTransform.parse_redis_enrty(entry) for entry in storage.retrieve())
        count = loader.insert_batch(batch)
        logger.info(f"Insert {count} strings to ClickHouse.")


if __name__ == "__main__":
    init_etl()
