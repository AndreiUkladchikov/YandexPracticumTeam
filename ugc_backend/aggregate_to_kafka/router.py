from __future__ import annotations

from aggregate_to_kafka.dependency import get_kafka
from aggregate_to_kafka.kafka_connector import send_data
from aggregate_to_kafka.schemas import Item, ResponseModel
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends

from core.config import settings

router = APIRouter()


@router.post(
    "",
    summary="Put views time",
    description="Put the user's movie viewing time to kafka",
    response_model=ResponseModel,
)
async def film_views(
    request_model: Item, producer: AIOKafkaProducer = Depends(get_kafka)
):
    key = request_model.user_id + "+" + request_model.film_id
    await send_data(
        value=str(request_model.timestamp).encode("utf-8"),
        key=key.encode("utf-8"),
        topic=settings.kafka_topic,
        producer=producer,
    )
    return ResponseModel(msg="OK")
