from __future__ import annotations

import time

from aioredis import Redis
from config import test_settings

if __name__ == "__main__":
    redis_host = test_settings.redis_host
    redis_conn = Redis(redis_host, socket_connect_timeout=1)
    while True:
        if redis_conn.ping():
            break
        time.sleep(1)
