from __future__ import annotations

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Person(BaseModel):
    id: str
    full_name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonDetailed(Person):
    actor_in: list[str] | None
    director_in: list[str] | None
    writer_in: list[str] | None
