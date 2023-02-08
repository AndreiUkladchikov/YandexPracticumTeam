import abc
import redis

from common.config import settings


class BaseStorage:

    @abc.abstractmethod
    def save(self, value: str) -> None:
        """Сохранить значение в хранилище."""
        pass

    @abc.abstractmethod
    def retrieve(self) -> str:
        """Загрузить значения из хранилища."""
        pass


class RedisStorage(BaseStorage):
    """Собирает батч для загрузки в ClickHouse."""

    def __init__(self):
        self.redis = redis.StrictRedis(host=settings.redis_storage.host,
                                       port=settings.redis_storage.port,
                                       charset='utf-8',
                                       decode_responses=True)
        self.list_key = settings.redis_list_key

    def save(self, value: str) -> None:
        """Добавляем значение в список Redis.

        Args:
            value (str): значение для добавления в список.
        """
        self.redis.rpush(self.list_key, value)

    def retrieve(self) -> str:
        """Читаем все значения из списка Redis."""
        for _ in range(self.redis.llen(self.list_key)):
            yield self.redis.lpop(self.list_key)
