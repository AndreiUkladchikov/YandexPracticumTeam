class DataTransform:

    @staticmethod
    def parse_kafka_data(key: str, value: str) -> str:
        """Парсим данные из Kafka."""
        entry = key.split("+")
        entry.append(value)
        return ",".join(entry)

    @staticmethod
    def parse_storage_enrty(entry: str) -> tuple[str, str, int]:
        """Парсим данные из хранилища."""
        user_id, film_id, timestamp = entry.split(",")
        return user_id, film_id, int(timestamp)
