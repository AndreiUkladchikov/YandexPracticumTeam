from __future__ import annotations

import math
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from api.constants.error_msgs import FilmMsg
from api.models.models import Film, FilmExtended, FilmsWithPaging
from core.config import settings
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    "",
    response_model=FilmsWithPaging,
    summary="Get Films",
    description="Get list of films (page by page)",
)
async def films_main_page(
    request: Request,
    sort: str = Query(default="-imdb_rating", regex="^-?imdb_rating$"),
    page_number: int | None = Query(default=1, alias="page[number]", ge=1),
    page_size: int
    | None = Query(default=settings.pagination_size, alias="page[size]", ge=1),
    genre: str | None = Query(None, alias="filter[genre]"),
    film_service: FilmService = Depends(get_film_service),
) -> FilmsWithPaging:
    url = request.url.path + "?" + request.url.query
    films, total_items = await film_service.get_films_main_page(
        url, sort, genre, page_number, page_size
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FilmMsg.no_search_result,
        )

    total_pages = math.ceil(total_items / page_size)

    return FilmsWithPaging(
        films=[Film(**film.dict()) for film in films],
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get(
    "/search",
    response_model=FilmsWithPaging,
    summary="Search Films",
    description="Get list of films by search criteria",
)
async def search_films(
    request: Request,
    query: str,
    page_number: int | None = Query(default=1, alias="page[number]", ge=1),
    page_size: int
    | None = Query(default=int(settings.pagination_size), alias="page[size]", ge=1),
    film_service: FilmService = Depends(get_film_service),
) -> FilmsWithPaging:
    url = request.url.path + "?" + request.url.query
    films, total_items = await film_service.search(url, query, page_number, page_size)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FilmMsg.no_search_result,
        )

    total_pages = math.ceil(total_items / page_size)

    return FilmsWithPaging(
        films=[Film(**film.dict()) for film in films],
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get(
    "/{film_id}/",
    response_model=FilmExtended,
    summary="Get Film by ID",
    description="Get full Film details by film ID",
)
async def film_details(
    request: Request,
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
) -> FilmExtended:
    url = request.url.path + request.url.query
    film = await film_service.get_by_id(url, film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=FilmMsg.not_found_by_id
        )
    return FilmExtended(**film.dict())
