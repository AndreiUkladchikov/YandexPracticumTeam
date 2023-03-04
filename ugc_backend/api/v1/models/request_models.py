from pydantic import BaseModel, Field

from models.likes import Rating


class LikeRequest(BaseModel):
    rating: Rating


class RatingRequest(BaseModel):
    rating: int = Field(ge=1, le=10)


class ReviewTextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=7000)
