from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models.reviews import Likes, Review


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(..., alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    id: uuid.UUID | None = None


class AboutFilm(BaseModel):
    film_id: str
    likes: Likes | None
