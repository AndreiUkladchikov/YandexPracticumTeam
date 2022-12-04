from __future__ import annotations

import json
import pickle
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import parse_obj_as

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonDetailed

PERSON_CACHE_EXPIRE_IN_SECONDS = settings.CACHE_EXPIRE_IN_SECONDS


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "persons"

    async def get_by_id(self, url: str, person_id: str) -> PersonDetailed | None:
        person = await self._person_from_cache(url)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(url, person)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> PersonDetailed | None:
        try:
            doc = await self.elastic.get(index=self.index, id=person_id)
        except NotFoundError:
            return None
        return PersonDetailed(**doc["_source"])

    async def _person_from_cache(self, url: str) -> PersonDetailed | None:
        data = await self.redis.get(url)
        if not data:
            return None
        person = PersonDetailed.parse_raw(data)
        return person

    async def _put_person_to_cache(self, url: str, person: PersonDetailed):
        await self.redis.set(
            url, person.json(), expire=PERSON_CACHE_EXPIRE_IN_SECONDS
        )

    async def search(
        self, url: str, query: str, page_number: int, page_size: int
    ) -> list[PersonDetailed] | None:
        persons = await self._person_search_from_cache(url)
        if not persons:
            persons = await self._search_from_elastic(query, page_number, page_size)
            if not persons:
                return None
            await self._put_person_search_to_cache(url, persons)
            print(url, persons)
        return persons

    async def _search_from_elastic(self, query: str, page_number: int, page_size: int):
        body = {
            "query": {"match": {"full_name": {"query": query, "fuzziness": "auto"}}}
        }
        try:
            persons = await self.elastic.search(
                index=self.index,
                body=body,
                from_=(page_number - 1) * page_size,
                size=page_size,
            )
        except NotFoundError:
            return None
        return [PersonDetailed(**p["_source"]) for p in persons["hits"]["hits"]]

    async def _person_search_from_cache(self, url: str) -> list[PersonDetailed] | None:
        data = await self.redis.get(url)
        if not data:
            return None
        persons = parse_obj_as(list[PersonDetailed], [json.loads(d) for d in pickle.loads(data)])
        return persons

    async def _put_person_search_to_cache(self, url: str, persons: list[PersonDetailed]):
        await self.redis.set(
            url, pickle.dumps([p.json() for p in persons]), expire=PERSON_CACHE_EXPIRE_IN_SECONDS
        )


def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
