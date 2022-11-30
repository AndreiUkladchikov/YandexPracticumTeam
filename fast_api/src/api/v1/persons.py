from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service
from services.transformation import person_transformation
from api.models.models import Film, PersonExtended
from core.config import settings
router = APIRouter()


@router.get("/search", response_model=list[PersonExtended])
async def person_details(
    query: str,
    page_number: int | None = Query(alias="page[number]", ge=1, default=1),
    page_size: int | None = Query(alias="page[size]", ge=1, default=settings.PAGINATION_SIZE),
    person_service: PersonService = Depends(get_person_service),
):
    persons = await person_service.search(query, page_number, page_size)

    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Persons  with your criteria not found")
    return [person_transformation(person) for person in persons]


@router.get("/{person_id}", response_model=PersonExtended)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonExtended:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")
    return person_transformation(person)


@router.get("/{person_id}/film", response_model=list[Film])
async def movies_by_person(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    person = await person_details(person_id, person_service)

    films = await films_by_id(person, film_service)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films with this person not found")
    return films


async def films_by_id(person: PersonExtended, film_service: FilmService) -> list[Film]:
    films: list[Film] = []
    for ids in person.film_ids:
        films.append(await film_service.get_by_id(ids))
    return films
