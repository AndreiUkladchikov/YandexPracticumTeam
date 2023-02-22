from __future__ import annotations

from enum import Enum

from models.parent_model import BaseOrjsonModel


class UserInfo(BaseOrjsonModel):
    user_id: str


class CountLikes(BaseOrjsonModel):
    count: int
    ids: list[str]


class Likes(BaseOrjsonModel):
    up: CountLikes | None
    down: CountLikes | None


class UserLikes(Likes):
    user_id: str


class AverageRating(BaseOrjsonModel):
    rating: float


class Rating(str, Enum):
    up = 10
    down = 1
