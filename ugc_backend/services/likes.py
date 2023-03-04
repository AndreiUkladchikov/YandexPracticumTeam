from __future__ import annotations

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from db.mongo import get_mongo
from helpers.custom_exceptions import FilmNotFound, ThereIsNoLikeToDelete
from helpers.likes import add_dislike, add_like, average, delete_like
from models.db_models import AboutFilm
from models.likes import AverageRating, Likes, Rating


class LikeService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo_client = mongo
        self.db = self.mongo_client[settings.mongo_db]
        self.collection = self.db[settings.like_collection]

    async def get_likes(self, film_id: str) -> Likes:
        result = await self.collection.find_one({"film_id": film_id})

        return Likes(**result["likes"]) if result else Likes()

    async def put_like(self, film_id: str, user_id: str, rating: Rating):
        """Добавление лайка."""
        doc: dict = await self.collection.find_one({"film_id": {"$eq": film_id}})
        result_likes: Likes = Likes()
        doc = doc if doc else AboutFilm(film_id=film_id).dict()
        if rating == Rating.up:
            result_likes = add_like(AboutFilm(**doc).likes, user_id)

        elif rating == Rating.down:
            result_likes = add_dislike(AboutFilm(**doc).likes, user_id)
        _ = await self.collection.update_one(
            {"film_id": film_id}, {"$set": {"likes": result_likes.dict()}}, upsert=True
        )

    async def delete_like(self, film_id: str, user_id: str):
        doc: dict = await self.collection.find_one({"film_id": {"$eq": film_id}})
        if doc:
            result_likes = delete_like(AboutFilm(**doc).likes, user_id)
            _ = await self.collection.update_one(
                {"film_id": film_id}, {"$set": {"likes": result_likes}}
            )
        else:
            raise ThereIsNoLikeToDelete

    async def average_rating(self, film_id: str) -> AverageRating:
        doc: dict = await self.collection.find_one({"film_id": {"$eq": film_id}})
        if doc:
            res_rating = average(doc)
            return AverageRating(rating=res_rating)
        else:
            raise FilmNotFound


def get_like_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> LikeService:
    return LikeService(mongo)
