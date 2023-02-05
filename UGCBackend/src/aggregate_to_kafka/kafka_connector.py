import http

import kafka.errors
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import HTTPException
from src.config import settings
from src.custom_log import logger


async def send_data(value: bytes, key: bytes):
    producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}"
    )

    # Get cluster layout and initial topic/partition leadership information
    try:
        await producer.start()
        # Produce message
        await producer.send_and_wait(f"{settings.kafka_topic}", value=value, key=key)
    except kafka.errors.KafkaConnectionError as kafka_error:
        logger.critical(kafka_error)
        raise HTTPException(
            status_code=http.HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Service is not available now :(",
        )
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


async def consume_data():
    consumer = AIOKafkaConsumer(
        f"{settings.kafka_topic}",
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
