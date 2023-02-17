from datetime import datetime

from models.likes import Likes, Rating
from models.parent_model import BaseOrjsonModel


class Review(BaseOrjsonModel):
    text: str
    publication_date: datetime
    author: str
    review_likes: Likes
    film_rating: Rating
