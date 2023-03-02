from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

mongo_client: Optional[AsyncIOMotorClient] = None


# Функция понадобится при внедрении зависимостей
async def get_mongo() -> AsyncIOMotorClient:
    return mongo_client
