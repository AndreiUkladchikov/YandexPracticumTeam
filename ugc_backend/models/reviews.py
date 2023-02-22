from datetime import datetime
from uuid import uuid4

from models.likes import Likes, Rating
from models.parent_model import BaseOrjsonModel
from pydantic import Field


class Review(BaseOrjsonModel):
    id: uuid4 = Field(default=uuid4())
    user_id: str
    publication_date: datetime = Field(default=datetime.now())
    mark: Rating
    text: str
    review_evaluation: Likes
