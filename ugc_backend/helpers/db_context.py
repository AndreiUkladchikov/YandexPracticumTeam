from __future__ import annotations

from core.custom_log import logger
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor


class DbContext:
    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self.mongo_collection = mongo_collection

    async def put_data(self, movie_id, user_id, rating):
        # logger.info(document)
        # document = {
        #     "film_id": f"{movie_id}",
        #     "likes": {rating.name: {"count": 1, "ids": [user_id]}},
        # }
        await self.mongo_collection.update_one(
            {"film_id": f"{movie_id}"}, {"$inc": {"up": 1}}, upsert=True
        )
        # logger.info(r.inserted_id)

    async def get_data(self, key, value) -> dict:
        result = [doc async for doc in self.mongo_collection.find({key: value})]

        logger.info(result)
        return result[0]
