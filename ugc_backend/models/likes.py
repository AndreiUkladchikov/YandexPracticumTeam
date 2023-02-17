from enum import Enum

from models.parent_model import BaseOrjsonModel


class Likes(BaseOrjsonModel):
    likes: int
    dislikes: int


class AverageRating(BaseOrjsonModel):
    rating: float


class Rating(str, Enum):
    like = 10
    dislike = 1
