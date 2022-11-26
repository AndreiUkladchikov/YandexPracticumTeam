from __future__ import annotations

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonDetailed


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # секунда


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> PersonDetailed | None:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> PersonDetailed | None:
        try:
            doc = await self.elastic.get(index="persons", id=person_id)
        except NotFoundError:
            return None
        return PersonDetailed(**doc["_source"])

    async def _person_from_cache(self, person_id: str) -> PersonDetailed | None:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = PersonDetailed.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: PersonDetailed):
        await self.redis.set(
            person.id, person.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )


def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
