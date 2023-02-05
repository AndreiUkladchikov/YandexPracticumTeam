from __future__ import annotations

from fastapi import APIRouter
from src.aggregate_to_kafka.kafka_connector import send_data
from src.aggregate_to_kafka.schemas import FilmViews, Item, ResponseModel
from src.aggregate_to_kafka.service import get_data_from_film_service
from src.schemas import Film

router = APIRouter()


@router.post(
    "",
    summary="Put views time",
    description="Put the user's movie viewing time to kafka",
)
async def film_views(request_model: Item):
    film_from_film_service: Film | None = await get_data_from_film_service(
        film_id=request_model.film_id
    )

    if film_from_film_service:
        film_view: FilmViews = FilmViews(
            **film_from_film_service.dict(), **request_model.dict()
        )
    else:
        film_view: FilmViews = FilmViews(
            **request_model.dict(), id=request_model.film_id, title=None
        )

    await send_data(
        value=film_view.json().encode("utf-8"), key=film_view.id.encode("utf-8")
    )

    return ResponseModel(msg="OK")
