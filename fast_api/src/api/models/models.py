from __future__ import annotations  # Для обратной совместимости с 3.8 и ниже

from enum import Enum

import orjson

from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    uuid: str = Field(alias="id")  # в ES у нас id вместо uuid
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonRole(str, Enum):
    actor = "actor"
    writer = "writer"
    director = "director"


class Person(BaseModel):
    uuid: str = Field(alias="id")  # в ES у нас id вместо uuid
    full_name: str

    class Config:
        use_enum_values = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonExtended(Person):
    role: set[PersonRole] | None
    film_ids: list[str] | None


class Film(BaseModel):
    uuid: str = Field(alias="id")  # в ES у нас id вместо uuid
    title: str
    imdb_rating: float | None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmExtended(Film):
    description: str | None
    genres: list[Genre] | None
    actors: list[Person] | None
    writers: list[Person] | None
    directors: list[Person] | None
