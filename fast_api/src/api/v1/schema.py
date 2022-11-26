from __future__ import annotations

from pydantic import BaseModel


class Genre(BaseModel):
    id: str
    name: str | None


class Person(BaseModel):
    id: str
    full_name: str


class PersonDetailed(Person):
    actor_in: list[str] | None
    director_in: list[str] | None
    writer_in: list[str] | None


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float | None


class FilmDetailed(Film):
    description: str | None
    genres: list[Genre] | None
    actors: list[Person] | None
    writers: list[Person] | None
    directors: list[Person] | None
