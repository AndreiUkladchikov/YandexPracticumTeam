from __future__ import annotations

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(BaseOrjsonModel):
    id: str
    full_name: str


class Genre(BaseOrjsonModel):
    id: str
    name: str | None


class Film(BaseOrjsonModel):
    id: str
    title: str | None
    description: str | None
    imdb_rating: float | None
    genres: list[Genre] | None
    actors: list[Person] | None
    writers: list[Person] | None
    directors: list[Person] | None
