import ast


class DataTransform:

    @staticmethod
    def parse_kafka_data(key: str, value: str) -> str:
        entry = key.split('+')
        entry.append(value)
        return ','.join(entry)

    @staticmethod
    def parse_redis_enrty(entry: str) -> tuple[str, ]:
        return ast.literal_eval(entry)
