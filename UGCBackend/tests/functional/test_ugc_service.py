import json

import requests
from src.config import settings
from tests.functional.constants import (
    test_data,
    test_invalid_timestamp,
    test_topic_name,
)

headers = {"Content-type": "application/json", "Accept": "text/plain"}


url_to_ugc = f"http://{settings.ugc_backend_host}:{settings.ugc_backend_port}/views"


class TestUGCService:
    def test_data(self):
        res = requests.post(url_to_ugc, headers=headers, data=json.dumps(test_data))
        assert res.status_code == 200

    def test_invalid_user_id(self):
        res = requests.post(
            url_to_ugc, headers=headers, data=json.dumps(test_topic_name)
        )
        assert res.status_code == 422

    def test_invalid_timestamp(self):
        res = requests.post(
            url_to_ugc, headers=headers, data=json.dumps(test_invalid_timestamp)
        )
        assert res.status_code == 422
