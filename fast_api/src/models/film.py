from __future__ import annotations

from models.genre import Genre
from models.parent_model import BaseOrjsonModel
from models.person import Person


class Film(BaseOrjsonModel):
    id: str
    title: str
    description: str | None
    imdb_rating: float | None
    genres: list[Genre] | None
    actors: list[Person] | None
    writers: list[Person] | None
    directors: list[Person] | None
