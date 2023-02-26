from __future__ import annotations

from core.config import settings
from db.mongo import get_mongo
from fastapi import Depends
from helpers.likes import add_dislike, add_like, average, delete_like
from models.likes import AverageRating, Likes, Rating
from motor.motor_asyncio import AsyncIOMotorClient


class LikeService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo_client = mongo
        self.db = self.mongo_client[settings.mongo_db]
        self.collection = self.db[settings.mongo_collection]

    async def get_likes(self, film_id: str) -> Likes:
        result = await self.collection.find_one({"film_id": film_id})

        return Likes(**result["likes"]) if result else Likes()

    async def put_like(self, film_id: str, user_id: str, rating: Rating):
        """Добавление лайка."""
        doc: dict = await self.collection.find_one({"film_id": {"$eq": film_id}})
        result_likes: dict = {}
        if rating == Rating.up:
            result_likes: dict = add_like(doc, user_id)

        elif rating == Rating.down:
            result_likes: dict = add_dislike(doc, user_id)

        _ = await self.collection.update_one(
            {"film_id": film_id}, {"$set": {"likes": result_likes}}, upsert=True
        )

    async def delete_like(self, film_id: str, user_id: str):
        doc: dict = await self.collection.find_one({"film_id": {"$eq": film_id}})
        result_likes = delete_like(doc, user_id)
        _ = await self.collection.update_one(
            {"film_id": film_id}, {"$set": {"likes": result_likes}}
        )

    async def average_rating(self, film_id: str) -> AverageRating:
        doc: dict = await self.collection.find_one({"film_id": {"$eq": film_id}})
        res_rating = average(doc)
        return AverageRating(rating=res_rating)


def get_like_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> LikeService:
    return LikeService(mongo)
