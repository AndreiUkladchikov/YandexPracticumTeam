from __future__ import annotations

import datetime

from models.likes import Likes, RatingInt
from pydantic import BaseModel, Field


class Review(BaseModel):
    review_id: str = ...
    user_id: str
    created: datetime.datetime = Field(default=datetime.datetime.utcnow())
    mark: RatingInt
    text: str
    review_evaluation: Likes | None = {}
