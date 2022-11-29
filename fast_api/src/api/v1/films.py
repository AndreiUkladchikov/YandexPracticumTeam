from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from api.models.models import FilmExtended, Film
from services.film import FilmService, get_film_service

router = APIRouter()

# ToDo: Genre model from Elastic should map to response Genre model


@router.get("/", response_model=list[Film])
async def film_details(
    sort: str, film_service: FilmService = Depends(get_film_service)
) -> list[Film]:
    films = await film_service.get_films_main_page(sort)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return [Film(**film.dict()) for film in films]


@router.get("/{film_id}", response_model=FilmExtended)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmExtended:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return FilmExtended(**film.dict())
