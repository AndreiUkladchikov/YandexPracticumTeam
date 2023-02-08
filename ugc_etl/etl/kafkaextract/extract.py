from __future__ import annotations

from time import sleep
from typing import Iterator

from confluent_kafka import Consumer
from loguru import logger

from common.config import settings
from common.decorators import backoff


class KafkaExtractor:
    """Извлекает данные из топика Kafka пачками указаного размера.

    consumer_config: dict[str, str] - настройки Kafka Consumer с указанием брокера, группы и отключением автокомита;
    topic: str - топик Kafka для чтения;
    batch_size: int - размер пачки данных, которую забираем из Kafka;
    sleep_timeout: int - таймаут ожидания новых сообщений в топике в секундах, при их отсутствии.
    """

    consumer_config = {
        'bootstrap.servers': settings.kafka_broker,
        'group.id': settings.kafka_group_id,
        'auto.offset.reset': 'largest',
        'enable.auto.commit': 'false',
        'max.poll.interval.ms': '86400000'
    }
    topic = settings.kafka_topic
    batch_size = settings.batch_size
    sleep_timeout = settings.kafka_sleep_timeout

    def __init__(self) -> None:
        """Создаем инстанс Kafka Consumer и подписываемся на топик."""
        consumer = Consumer(self.consumer_config)
        consumer.subscribe([self.topic])
        self.consumer = consumer

    @backoff()
    def extract_batch(self) -> Iterator[tuple[str, ]]:
        """Выгружаем батч указаного размера из Kafka.

        Raises:
            e: Исключение, обрабатывается и логируется в backoff.

        Yields:
            Iterator[tuple[str, ]]: кортеж (ключ, значение) из топика.
        """
        count = 0
        try:
            while count < self.batch_size:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    logger.info(f'Waiting for message or event/error in poll() {self.sleep_timeout} sec.')
                    sleep(self.sleep_timeout)
                    continue
                elif msg.error():
                    logger.error(f'Error: {msg.error()}.')
                else:
                    count += 1
                    yield msg.key().decode('utf-8'), msg.value().decode('utf-8')
        except Exception as e:
            # Прокидываем ошибку в backoff
            raise e
        else:
            # Фиксируем offset при успешной выгрузке пачки указаного размера
            self.consumer.commit()
        finally:
            # Закрываем consumer
            self.consumer.close()
