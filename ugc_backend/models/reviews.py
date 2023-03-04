from __future__ import annotations

import datetime

from pydantic import BaseModel, Field

from models.likes import Likes, RatingInt


class Review(BaseModel):
    film_id: str
    review_id: str = ...
    user_id: str
    created: datetime.datetime = Field(default=datetime.datetime.utcnow())
    mark: RatingInt
    text: str
    review_evaluation: Likes | None = Likes()


class ReviewResponse(BaseModel):
    review_id: str
