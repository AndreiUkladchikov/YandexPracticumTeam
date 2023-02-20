from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Up:
    ids: list[UUID, ]
    count: int = 0


@dataclass
class Down:
    ids: list[UUID, ]
    count: int = 0


@dataclass
class Likes:
    up: Up
    down: Down


@dataclass
class ReviewEvaluation:
    up: Up
    down: Down


@dataclass
class Review:
    id: UUID
    user_id: UUID
    firstname: str
    lastname: str
    created: datetime
    mark: int
    text: str
    review_evaluation: ReviewEvaluation


@dataclass
class FilmUserRate:
    film_id: UUID
    reviews: list[Review, ]
    likes: Likes
