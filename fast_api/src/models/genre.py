from __future__ import annotations

from models.parent_model import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    id: str
    name: str | None
