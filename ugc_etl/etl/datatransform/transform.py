class DataTransform:

    @staticmethod
    def parse_kafka_data(key: str, value: str) -> str:
        """Парсит данные в сообщении из Kafka для дальнейшей загрузки в Redis."""
        entry = key.split('+')
        entry.append(value)
        return ','.join(entry)

    @staticmethod
    def parse_redis_entry(entry: str) -> tuple[str, str, int]:
        """Парсит данные из Redis для загрузки в ClickHouse."""
        user_id, film_id, timestamp = entry.split(',')
        return user_id, film_id, int(timestamp)
