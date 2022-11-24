from typing import Optional
from elasticsearch_async import AsyncElasticsearch

es: Optional[AsyncElasticsearch] = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return es
