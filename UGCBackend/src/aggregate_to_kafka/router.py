from __future__ import annotations

from fastapi import APIRouter
from src.aggregate_to_kafka.kafka_connector import send_data
from src.aggregate_to_kafka.schemas import Item, ResponseModel

router = APIRouter()


@router.post(
    "",
    summary="Put views time",
    description="Put the user's movie viewing time to kafka",
)
async def film_views(request_model: Item):
    key = request_model.user_id + "+" + request_model.film_id

    await send_data(value=request_model.json().encode("utf-8"), key=key.encode("utf-8"))

    return ResponseModel(msg="OK")
