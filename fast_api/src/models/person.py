from __future__ import annotations

from models.parent_model import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: str
    full_name: str


class PersonDetailed(Person):
    actor_in: list[str] | None
    director_in: list[str] | None
    writer_in: list[str] | None
