from __future__ import annotations
from uuid import uuid4

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from db.mongo import get_mongo
from helpers.custom_exceptions import FilmNotFound, ReviewNotFound
from helpers.likes import add_dislike, add_like
from models.likes import Likes, Rating
from models.reviews import Review
from services.likes import LikeService


class ReviewService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo_client = mongo
        self.db = self.mongo_client[settings.mongo_db]
        self.review_collection = self.db[settings.reviews_collection]

    async def get_all_reviews(
        self, film_id: str, sort: str, page_size: int
    ) -> list[Review] | None:
        if sort.startswith("-"):
            doc: list = [
                doc
                async for doc in self.review_collection.find(
                    {"film_id": {"$eq": film_id}},
                    sort=[("review_evaluation.up.count", -1)],
                    limit=page_size,
                )
            ]
        else:
            doc: list = [
                doc
                async for doc in self.review_collection.find(
                    {"film_id": {"$eq": film_id}},
                    sort=[("review_evaluation.up.count", 1)],
                    limit=page_size,
                )
            ]

        if doc:
            return [Review(**rev) for rev in doc]
        else:
            raise FilmNotFound

    async def add_like_to_review(
        self, film_id: str, user_id: str, review_id: str, rating: Rating
    ):
        doc: dict | None = await self.review_collection.find_one(
            {"review_id": {"$eq": review_id}}
        )
        if not doc:
            raise ReviewNotFound
        result_likes: Likes = Likes()
        if rating == Rating.up:
            result_likes = add_like(Review(**doc).review_evaluation, user_id)

        elif rating == Rating.down:
            result_likes = add_dislike(Review(**doc).review_evaluation, user_id)

        _ = await self.review_collection.update_one(
            {"review_id": review_id},
            {"$set": {"review_evaluation": result_likes.dict()}},
            upsert=True,
        )

    async def add_review(
        self,
        film_id: str,
        user_id: str,
        text: str,
        rating: Rating,
        like_service: LikeService,
    ):
        await like_service.put_like(film_id, user_id, rating)
        review_id = str(uuid4())
        review = Review(
            film_id=film_id,
            review_id=review_id,
            user_id=user_id,
            text=text,
            mark=int(rating),
        )
        await self.review_collection.insert_one(
            review.dict(),
        )
        return {"review_id": review_id}


def get_review_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> ReviewService:
    return ReviewService(mongo)
