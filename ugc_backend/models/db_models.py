from __future__ import annotations

from pydantic import BaseModel

from models.reviews import Likes


class AboutFilm(BaseModel):
    film_id: str
    likes: Likes | None
