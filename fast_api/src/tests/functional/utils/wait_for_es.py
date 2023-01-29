from __future__ import annotations

import time

from config import test_settings
from elasticsearch import AsyncElasticsearch

if __name__ == "__main__":
    es_client = AsyncElasticsearch(hosts=test_settings.es_host)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
