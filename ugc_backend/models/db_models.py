from __future__ import annotations

from datetime import datetime
from typing import Optional

from models.reviews import Likes, Review
from pydantic import BaseModel, Field


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(..., alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    id: Optional[int] = None


class AboutFilm(BaseModel):
    film_id: str
    reviews: list[Review] | None
    likes: Likes | None
