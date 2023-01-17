from __future__ import annotations

import uuid
from enum import Enum

from pydantic import BaseModel


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    actor_in: list | None = []
    writer_in: list | None = []
    director_in: list | None = []


class NestedModel(BaseModel):
    id: uuid.UUID
    name: str


class NestedModelPerson(BaseModel):
    id: uuid.UUID
    full_name: str


class Movie(BaseModel):
    id: uuid.UUID
    imdb_rating: float | None = 0.0
    type: str
    title: str
    description: str | None = ''
    director: str
    actors_names: list
    writers_names: list
    actors: list
    writers: list
    genres: list
    genre: list
    directors: list


class PersonTypes(str, Enum):
    ACTOR = 'actor'
    DIRECTOR = 'director'
    WRITER = 'writer'
