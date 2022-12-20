from __future__ import annotations

import math
from http import HTTPStatus

from api.constants.error_msgs import ElasticMsg, GenreMsg
from api.models.models import Genre, GenresWithPaging
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from repository.custom_exceptions import ElasticSearchIsNotAvailable
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    "/",
    response_model=GenresWithPaging,
    summary="Get Genres",
    description="Get list of genres (page by page)",
)
async def genre_list(
    request: Request,
    page_number: int
    | None = Query(alias="page[number]", ge=1, default=1, le=settings.max_page_number),
    page_size: int
    | None = Query(
        alias="page[size]",
        ge=1,
        default=settings.pagination_size,
        le=settings.max_page_size,
    ),
    film_service: GenreService = Depends(get_genre_service),
) -> GenresWithPaging:
    url = request.url.path + "?" + request.url.query
    try:
        genres, total_items = await film_service.get_list_genres(
            url, page_number, page_size
        )
    except ElasticSearchIsNotAvailable:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ElasticMsg.elasticsearch_is_not_available,
        )

    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=GenreMsg.no_search_result
        )

    total_pages = math.ceil(total_items / page_size)

    return GenresWithPaging(
        genres=genres, total_pages=total_pages, total_items=total_items
    )


@router.get("/{genre_id}", response_model=Genre, description="Get Genre by ID")
async def genre_details(
    request: Request,
    genre_id: str,
    film_service: GenreService = Depends(get_genre_service),
) -> Genre:
    url = request.url.path + "?" + request.url.query
    try:
        genre = await film_service.get_genre_by_id(url, genre_id)
    except ElasticSearchIsNotAvailable:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ElasticMsg.elasticsearch_is_not_available,
        )
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=GenreMsg.not_found_by_id
        )
    return genre
