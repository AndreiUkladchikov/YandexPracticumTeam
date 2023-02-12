from __future__ import annotations


class DataTransform:
    @staticmethod
    def parse_kafka_data(key: str, value: str) -> str:
        entry = key.split("+")
        entry.append(value)
        return ",".join(entry)

    @staticmethod
    def parse_redis_enrty(entry: str) -> tuple[str, str, int]:
        user_id, film_id, timestamp = entry.split(",")
        return user_id, film_id, int(timestamp)
