from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from api.models.models import FilmExtended, Film
from core.config import settings
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get("", response_model=list[Film])
async def films_main_page(
        sort: str = Query(default='-imdb_rating', regex="^-?imdb_rating$"),
        page_number: int | None = Query(default=1, alias="page[number]", ge=1),
        page_size: int | None = Query(default=int(settings.PAGINATION_SIZE), alias="page[size]", ge=1),
        genre: str | None = Query(None, alias="filter[genre]"),
        film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.get_films_main_page(sort, genre, page_number, page_size)
    return [Film(**film.dict()) for film in films]


@router.get("/search", response_model=list[Film])
async def search_films(
        query: str,
        page_number: int | None = Query(default=1, alias="page[number]", ge=1),
        page_size: int | None = Query(default=int(settings.PAGINATION_SIZE), alias="page[size]", ge=1),
        film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.search(query, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films with your criteria not found")
    return [Film(**film.dict()) for film in films]


@router.get("/{film_id}/", response_model=FilmExtended)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmExtended:

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")
    return FilmExtended(**film.dict())
