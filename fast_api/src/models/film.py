from __future__ import annotations

import orjson

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel

from models.genre import Genre
from models.person import Person


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: str
    title: str
    description: str | None
    imdb_rating: float | None
    genres: list[Genre] | None
    actors: list[Person] | None
    writers: list[Person] | None
    directors: list[Person] | None

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps
