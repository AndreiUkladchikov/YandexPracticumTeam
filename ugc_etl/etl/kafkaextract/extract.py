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

    def __init__(self,
                 broker: str = settings.kafka_broker,
                 group_id: str = settings.kafka_group_id,
                 topic: str = settings.kafka_topic,
                 sleep_timeout: int = settings.kafka_sleep_timeout) -> None:
        """Создаем инстанс Kafka Consumer и подписываемся на топик.

        Args:
            broker (str, optional): Kafka host and port.
            group_id (str, optional): Kafka consumer group id.
            topic (str, optional): Kafka topic.
            sleep_timeout (int, optional): timeout in seconds for new messages.
        """

        consumer_config = {
            "bootstrap.servers": broker,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": "false",
        }
        consumer = Consumer(**consumer_config)
        consumer.subscribe(
            [
                topic,
            ]
        )
        self.consumer = consumer
        self.sleep_timeout = sleep_timeout

    def extract_batch(
        self, batch_size: int
    ) -> Iterator[tuple[str, ]]:
        """Выгружаем записи из Kafka.

        Raises:
            e: Исключение, обрабатывается и логируется в backoff.

        Yields:
            Iterator[tuple[str, ]]: кортеж (ключ, значение) из топика.
        """
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
                yield msg.key().decode("utf-8"), msg.value().decode("utf-8")
        self.consumer.commit()
