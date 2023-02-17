from db.mongo import get_mongo
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient


class LikeService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo_client = mongo

    def get_likes(self, film_id: str):
        pass


def get_like_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> LikeService:
    return LikeService(mongo)
