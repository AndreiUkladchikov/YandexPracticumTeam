from enum import Enum

import orjson

from pydantic import BaseModel, Field, validator, root_validator


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    uuid: str = Field(alias='id')
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonRole(str, Enum):
    actor = 'actor'
    writer = 'writer'
    director = 'director'


class PersonShortInfo(BaseModel):
    uuid: str = Field(alias='id')
    full_name: str

    class Config:
        use_enum_values = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonDetailedInfo(PersonShortInfo):
    roles: list[PersonRole] | None
    film_ids: list[str] | None

    class Config:
        use_enum_values = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmShortInfo(BaseModel):
    uuid: str = Field(alias='id')
    title: str
    imdb_rating: float

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmDetailedInfo(FilmShortInfo):
    description: str
    genres: list[Genre]
    actors: list[PersonShortInfo]
    directors: list[PersonShortInfo]
    writers: list[PersonShortInfo]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
