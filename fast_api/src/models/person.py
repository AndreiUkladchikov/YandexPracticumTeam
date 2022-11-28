from __future__ import annotations

import orjson
from pydantic import BaseModel, root_validator


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PersonShortInfo(BaseModel):
    id: str
    full_name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(PersonShortInfo):
    actor_in: list[str] | None
    director_in: list[str] | None
    writer_in: list[str] | None
    roles: list[str] | None
    film_ids: list[str] | None

    @root_validator
    def set_film_ids_and_roles(cls, values):
        values['roles'] = [key[:-3] for key in values.keys() if key.endswith('_in')]
        values['film_ids'] = set(values['actor_in'] + values['director_in'] + values['writer_in'])
        return values

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
