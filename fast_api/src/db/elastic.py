from elasticsearch import AsyncElasticsearch

from db.protocols.db_protocol import DbProtocol


class ElasticDb(DbProtocol):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def _close(self):
        await self.elastic.close()

    async def _get_by_id(self, index: str, id: str):
        return await self.elastic.get(index=index, id=id)
