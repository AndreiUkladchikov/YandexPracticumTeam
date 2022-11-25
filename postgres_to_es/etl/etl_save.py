from typing import Any

from elasticsearch import Elasticsearch, helpers


def put_data(conn: str, data: Any) -> None:
    es = Elasticsearch(conn, timeout=300)
    helpers.bulk(es, data)
