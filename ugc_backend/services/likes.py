from core.config import settings
from core.custom_log import logger
from db.mongo import get_mongo
from fastapi import Depends
from helpers.db_context import DbContext
from models.likes import Likes, Rating
from motor.motor_asyncio import AsyncIOMotorClient


class LikeService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.db_context = DbContext(
            mongo_collection=mongo.mongo_client[settings.mongo_db].db[
                settings.mongo_collection
            ]
        )
        # self.mongo_client = mongo
        # self.db = self.mongo_client["myNewDB"]
        # self.collection = self.db["movies"]

    async def get_likes(self, movie_id: str) -> Likes:
        likes = await self.db_context.get_data(key="film_id", value=movie_id)
        logger.info(Likes(**likes))
        return Likes(**likes["likes"])

    async def put_like(self, movie_id: str, user_id: str, rating: Rating):
        # db = mongo.mongo_client.test_database
        # print(db)
        # document = await collection.find_one({'age': {'$gt': 1}})
        # document = {
        #     "film_id": f"{movie_id}",
        #     "likes": {rating.name: {"count": 1, "ids": [user_id]}},
        # }

        await self.db_context.put_data(movie_id, user_id, rating)
        # print('result %s' % repr(result.inserted_id))


def get_like_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> LikeService:
    return LikeService(mongo)
