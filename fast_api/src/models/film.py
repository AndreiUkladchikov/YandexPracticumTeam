from __future__ import annotations

import orjson

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel
from models.genre import Genre
from models.person import PersonShortInfo


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: str
    title: str
    type: str
    imdb_rating: float
    description: str | None
    director: str
    actors_names: list[str]
    writers_names: list[str]
    genres: list[Genre]
    genre: list[str]
    actors: list[PersonShortInfo]
    writers: list[PersonShortInfo]
    directors: list[PersonShortInfo]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
