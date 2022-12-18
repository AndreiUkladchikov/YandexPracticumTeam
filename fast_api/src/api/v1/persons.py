from __future__ import annotations

from http import HTTPStatus

import requests
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from api.models.models import Film, PersonExtended
from core.config import settings
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service
from services.transformation import person_transformation
from api.constants.error_msgs import PersonMsg

router = APIRouter()


@router.get(
    "/search",
    response_model=list[PersonExtended],
    summary='Search Persons',
    description='Get list of Persons by search criteria'
)
async def person_details(
    request: Request,
    query: str,
    page_number: int | None = Query(alias="page[number]", ge=1, default=1),
    page_size: int
    | None = Query(alias="page[size]", ge=1, default=settings.pagination_size),
    person_service: PersonService = Depends(get_person_service),
):
    url = request.url.path + request.url.query
    persons = await person_service.search(url, query, page_number, page_size)

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PersonMsg.no_search_result,
        )
    return [person_transformation(person) for person in persons]


@router.get(
    "/{person_id}",
    response_model=PersonExtended,
    summary='Get Person details',
    description='Get full Person details by ID'
)
async def person_details(
    request: Request,
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonExtended:
    url = request.url.path + request.url.query
    person = await person_service.get_by_id(url, person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PersonMsg.not_found_by_id
        )
    return person_transformation(person)


@router.get(
    "/{person_id}/film",
    response_model=list[Film],
    description='Get list of Films by Person'
)
async def movies_by_person(
    request: Request,
    person_id: str,
    page_number: int | None = Query(default=1, alias="page[number]", ge=1, le=200),
    page_size: int
    | None = Query(default=int(settings.pagination_size), alias="page[size]", ge=1, le=10000),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    url = request.url.path + request.url.query

    films = await film_service.get_films_by_person_id(url, page_number, page_size, person_id)

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PersonMsg.no_films_by_person
        )
    return films


async def films_by_id(person: PersonExtended, film_service: FilmService) -> list[Film]:
    films: list[Film] = []
    for ids in person.film_ids:
        films.append(await film_service.get_by_id(None, ids))
    return films
