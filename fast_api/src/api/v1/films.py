from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from api.models.models import FilmExtended
from services.film import FilmService, get_film_service

router = APIRouter()

# ToDo: Genre model from Elastic should map to response Genre model


@router.get("/{film_id}", response_model=FilmExtended)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmExtended:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return FilmExtended(**film.dict())
