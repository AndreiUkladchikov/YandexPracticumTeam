from __future__ import annotations

from core.custom_log import logger
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor


class DbContext:
    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self.mongo_collection = mongo_collection

    async def put_data(self, document: dict):
        logger.info(document)
        r = await self.mongo_collection.insert_one(document)
        logger.info(r.inserted_id)

    async def get_data(self, key, value) -> dict:
        result = [doc async for doc in self.mongo_collection.find({key: value})]

        logger.info(result)
        return result[0]
