from __future__ import annotations

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import WriteError

from core.config import settings
from db.mongo import get_mongo
from helpers.custom_exceptions import DuplicateFilm
from models.user_bookmarks import Bookmarks


class BookmarkService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo_client = mongo
        self.db = self.mongo_client[settings.mongo_db]
        self.bookmark_collection = self.db[settings.bookmarks_collection]

    async def all_bookmarks(self, user_id: str) -> Bookmarks:
        doc: dict = await self.bookmark_collection.find_one(
            {"user_id": {"$eq": user_id}}
        )
        if doc:
            return Bookmarks(**doc)
        else:
            return Bookmarks(user_id=user_id)

    async def add_bookmark(self, user_id: str, film_id: str):
        try:
            await self.bookmark_collection.update_one(
                {"user_id": {"$eq": user_id}},
                {"$push": {"film_id": film_id}},
                upsert=True,
            )
        except WriteError:
            raise DuplicateFilm

    async def delete_bookmark(self, user_id: str, film_id: str):
        await self.bookmark_collection.update_one(
            {"user_id": {"$eq": user_id}},
            {"$pull": {"film_id": {"$eq": film_id}}},
        )


def get_bookmark_service(
    mongo: AsyncIOMotorClient = Depends(get_mongo),
) -> BookmarkService:
    return BookmarkService(mongo)
