from typing import Any

from elasticsearch import Elasticsearch, helpers

import db_config

es = Elasticsearch(db_config.ELASTIC_CON, timeout=300)


def put_data(data: Any) -> None:
    helpers.bulk(es, data)
