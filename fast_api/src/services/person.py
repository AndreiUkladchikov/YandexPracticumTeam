from __future__ import annotations

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonDetailed
from repository.db_context import DbContext


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.db_context = DbContext(redis, elastic, "persons", settings.cache_expire_in_seconds)

    async def get_by_id(self, url: str, person_id: str) -> PersonDetailed | None:
        data = await self.db_context.get_by_id(url, person_id)
        if not data:
            return None

        person = PersonDetailed(**data["_source"])
        return person

    async def search(
        self, url: str, query: str, page_number: int, page_size: int
    ) -> list[PersonDetailed] | None:
        body = {
            "query": {"match": {"full_name": {"query": query, "fuzziness": "auto"}}}
        }
        doc = await self.db_context.get_list(url, page_number, page_size, body)
        if not doc:
            return None

        return [PersonDetailed(**person["_source"]) for person in doc["hits"]["hits"]]


def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
