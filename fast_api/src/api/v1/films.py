from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.models.models import FilmShortInfo, FilmDetailedInfo
from services.film import FilmService, get_film_service

router = APIRouter()

# ToDo: Genre model from Elastic should map to response Genre model


@router.get("/", response_model=list[FilmShortInfo])
async def film_main_page(
        sort: str, film_service: FilmService = Depends(get_film_service)
) -> list[FilmShortInfo]:
    films = await film_service.get_films_main_page(sort)
    return [FilmShortInfo(**film.dict()) for film in films]


@router.get("/{film_id}", response_model=FilmDetailedInfo)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmDetailedInfo:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return FilmDetailedInfo(**film.dict())
