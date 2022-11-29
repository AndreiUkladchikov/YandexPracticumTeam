from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service

from api.models.models import PersonDetailedInfo, FilmShortInfo
from services.transformation import person_transformation

router = APIRouter()

# ToDo: Person model from Elastic should map to response Person model


@router.get("/{person_id}", response_model=PersonDetailedInfo)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonDetailedInfo:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return person_transformation(person)


@router.get("/{person_id}/film", response_model=list[FilmShortInfo])
async def movies_by_person(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmShortInfo]:
    person = await person_service.get_by_id(person_id)

    films = await film_service.get_films_by_person(person)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")

    return [FilmShortInfo(**film.dict()) for film in films]
