from __future__ import annotations

from models.parent_model import BaseOrjsonModel


class Bookmarks(BaseOrjsonModel):
    user_id: str
    film_id: list[str] | None
