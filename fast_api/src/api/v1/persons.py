from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service

from api.v1.schema import PersonDetailed, Film

router = APIRouter()


@router.get("/{person_id}", response_model=PersonDetailed)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonDetailed:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")

    return PersonDetailed(**person.dict())


@router.get("/{person_id}/film", response_model=list[Film])
async def movies_by_person(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    person = await person_service.get_by_id(person_id)

    films = await film_service.get_films_by_person(person)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    print(films)

    return [
        Film(id=film.id, title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]
