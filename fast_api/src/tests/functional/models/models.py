from __future__ import annotations
from enum import Enum

from pydantic import BaseModel


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float | None


class Genre(BaseModel):
    id: str
    name: str


class PersonRole(str, Enum):
    actor = "actor"
    writer = "writer"
    director = "director"


class Person(BaseModel):
    id: str
    full_name: str
    role: set[PersonRole] | None
    film_ids: list[str] | None


class Response(BaseModel):
    body: dict | list
    status: int
