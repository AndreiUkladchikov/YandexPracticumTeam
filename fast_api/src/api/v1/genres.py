from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from services.genre import GenreService, get_genre_service
from core.config import settings
from api.models.models import Genre

router = APIRouter()


@router.get("/", response_model=list[Genre])
async def genre_list(
    page_number: int | None = Query(alias="page[number]", ge=1, default=1),
    page_size: int | None = Query(alias="page[size]", ge=1, default=settings.PAGINATION_SIZE),
    film_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    genres = await film_service.get_list_genres(page_number, page_size)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return genres


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(
    genre_id: str, film_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await film_service.get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return genre
