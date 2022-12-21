from __future__ import annotations

import math
from http import HTTPStatus

from api.constants.error_msgs import ElasticMsg, PersonMsg
from api.models.models import Film, FilmsWithPaging, PersonExtended
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from repository.custom_exceptions import ElasticSearchIsNotAvailable
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service
from services.transformation import person_transformation

router = APIRouter()


@router.get(
    "/search",
    response_model=list[PersonExtended],
    summary="Search Persons",
    description="Get list of Persons by search criteria",
)
async def person_details(
    request: Request,
    query: str,
    page_number: int
    | None = Query(alias="page[number]", ge=1, default=1, le=settings.max_page_number),
    page_size: int
    | None = Query(
        alias="page[size]",
        ge=1,
        default=settings.pagination_size,
        le=settings.max_page_size,
    ),
    person_service: PersonService = Depends(get_person_service),
):
    url = request.url.path + "?" + request.url.query
    try:

        persons = await person_service.search(url, query, page_number, page_size)
    except ElasticSearchIsNotAvailable:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ElasticMsg.elasticsearch_is_not_available,
        )

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PersonMsg.no_search_result,
        )
    return [person_transformation(person) for person in persons]


@router.get(
    "/{person_id}",
    response_model=PersonExtended,
    summary="Get Person details",
    description="Get full Person details by ID",
)
async def person_details(
    request: Request,
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
) -> PersonExtended:
    url = request.url.path + "?" + request.url.query
    try:
        person = await person_service.get_by_id(url, person_id)
    except ElasticSearchIsNotAvailable:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ElasticMsg.elasticsearch_is_not_available,
        )
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PersonMsg.not_found_by_id
        )
    return person_transformation(person)


@router.get(
    "/{person_id}/film",
    response_model=FilmsWithPaging,
    description="Get list of Films by Person",
)
async def movies_by_person(
    request: Request,
    person_id: str,
    page_number: int
    | None = Query(default=1, alias="page[number]", ge=1, le=settings.max_page_number),
    page_size: int
    | None = Query(
        default=int(settings.pagination_size),
        alias="page[size]",
        ge=1,
        le=settings.max_page_size,
    ),
    film_service: FilmService = Depends(get_film_service),
) -> FilmsWithPaging:

    url = request.url.path + request.url.query
    try:
        films, total_items = await film_service.get_films_by_person_id(
            url, page_number, page_size, person_id
        )
    except ElasticSearchIsNotAvailable:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ElasticMsg.elasticsearch_is_not_available,
        )

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PersonMsg.no_films_by_person
        )
    total_pages = math.ceil(total_items / page_size)

    return FilmsWithPaging(
        films=[Film(**film.dict()) for film in films],
        total_pages=total_pages,
        total_items=total_items,
    )
