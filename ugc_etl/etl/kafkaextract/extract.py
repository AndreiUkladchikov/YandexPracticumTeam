from __future__ import annotations

from time import sleep
from typing import Iterator

from common.config import settings
from confluent_kafka import Consumer
from loguru import logger


class KafkaExtractor:
    """Извлекает данные из топика Kafka.

    consumer_config: dict[str, str] - настройки Kafka Consumer с указанием брокера, группы и отключением автокомита;
    topic: str - топик Kafka для чтения;
    sleep_timeout: int - таймаут ожидания новых сообщений в топике в секундах, при их отсутствии.
    """

    consumer_config = {
        "bootstrap.servers": settings.kafka_broker,
        "group.id": settings.kafka_group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": "false",
    }
    topic = settings.kafka_topic
    sleep_timeout = settings.kafka_sleep_timeout

    def __init__(self) -> None:
        """Создаем инстанс Kafka Consumer и подписываемся на топик."""
        consumer = Consumer(**self.consumer_config)
        consumer.subscribe(
            [
                self.topic,
            ]
        )
        self.consumer = consumer

    def extract_batch(
        self, batch_size: int
    ) -> Iterator[tuple[str,]]:
        """Выгружаем записи из Kafka.

        Raises:
            e: Исключение, обрабатывается и логируется в backoff.

        Yields:
            Iterator[tuple[str, ]]: кортеж (ключ, значение) из топика.
        """
        try:
            counter = 0
            while counter < batch_size:
                msg = self.consumer.poll(1)
                if msg is None:
                    logger.info(
                        f"Fetched {counter}/{batch_size}. Waiting for message or event/error in poll() {self.sleep_timeout} sec."
                    )
                    sleep(self.sleep_timeout)
                    continue
                elif msg.error():
                    logger.error(f"Error: {msg.error()}.")
                else:
                    counter += 1
                    # logger.info(f'Message {msg.key().decode("utf-8")}: {msg.value().decode("utf-8")} extract.')
                    yield msg.key().decode("utf-8"), msg.value().decode("utf-8")
                    self.consumer.commit()
        finally:
            # Закрываем consumer
            self.consumer.close()
