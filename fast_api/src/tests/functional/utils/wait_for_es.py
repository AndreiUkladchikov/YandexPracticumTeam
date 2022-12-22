from __future__ import annotations

import time

from elasticsearch import AsyncElasticsearch

from config import test_settings

if __name__ == '__main__':
    es_client = AsyncElasticsearch(hosts=test_settings.es_host)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
