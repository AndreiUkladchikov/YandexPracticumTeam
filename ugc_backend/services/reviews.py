from uuid import uuid4

from db.mongo import get_mongo
from fastapi import Depends
from models.likes import Rating
from models.reviews import Review
from motor.motor_asyncio import AsyncIOMotorClient
from services.likes import LikeService


class ReviewService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo_client = mongo
        self.db = self.mongo_client["myNewDB"]
        self.collection = self.db["movies"]

    async def add_like_to_review(self, film_id: str, review_id: str, rating: Rating):
        pass

    async def add_review(
        self,
        film_id: str,
        user_id: str,
        text: str,
        rating: Rating,
        like_service: LikeService,
    ):
        await like_service.put_like(film_id, user_id, rating)

        review = Review(
            review_id=str(uuid4()), user_id=user_id, text=text, mark=int(rating)
        )
        await self.collection.update_one(
            {"film_id": {"$eq": film_id}},
            {"$addToSet": {"reviews": review.dict()}},
            upsert=True,
        )


def get_review_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> ReviewService:
    return ReviewService(mongo)
