import http

from aiokafka import AIOKafkaProducer, errors
from fastapi import HTTPException
from src.custom_log import logger


async def send_data(value: bytes, key: bytes, topic: str, producer: AIOKafkaProducer):
    try:
        await producer.send_and_wait(topic, value=value, key=key)
    except errors.KafkaConnectionError as kafka_error:
        logger.critical(kafka_error)
        raise HTTPException(
            status_code=http.HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Service is not available now :(",
        )
