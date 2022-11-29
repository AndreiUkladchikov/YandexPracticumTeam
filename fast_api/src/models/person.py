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
    actor_in: list[str]
    writer_in: list[str]
    director_in: list[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
