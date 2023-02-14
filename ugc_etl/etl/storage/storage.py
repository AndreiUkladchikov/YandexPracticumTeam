import abc
from typing import Iterator

import redis
from common.config import settings


class BaseStorage(abc.ABC):

    @abc.abstractmethod
    def save(self, value: str) -> None:
        """Сохранить значение в хранилище."""
        pass

    @abc.abstractmethod
    def retrieve(self) -> str:
        """Загрузить значения из хранилища."""
        pass

    @abc.abstractmethod
    def current_batch_size(self) -> int:
        """Возращает размер батча в хранилище."""
        pass


class RedisStorage(BaseStorage):
    """Собирает и хранит батч для загрузки в ClickHouse."""

    def __init__(self,
                 host: str = settings.redis_storage.host,
                 port: int = settings.redis_storage.port,
                 list_key: str = settings.redis_list_key) -> None:
        """Создаем подключение к Redis, получаем ключ списка.

        Args:
            host (str, optional): Redis host.
            port (int, optional): Redis port.
            list_key (str, optional): Key of list in Redis.
        """
        self.redis = redis.StrictRedis(
            host=host,
            port=port,
            charset="utf-8",
            decode_responses=True,
        )
        self.list_key = list_key

    def save(self, value: str) -> None:
        """Добавляем значение в список Redis.

        Args:
            value (str): значение для добавления в список.
        """
        self.redis.rpush(self.list_key, value)

    def retrieve(
        self,
    ) -> Iterator[str, ]:
        """Читаем все значения из списка Redis."""
        for _ in range(self.redis.llen(self.list_key)):
            yield self.redis.lpop(self.list_key)

    def current_batch_size(self) -> int:
        """Возращает размер батча в Redis."""
        return self.redis.llen(self.list_key)


class ListStorage(BaseStorage):

    def __init__(self) -> None:
        """Создаем пустой список в кором будем собирать батч."""
        self.list_storage = []

    def save(self, value: str) -> None:
        """Добавляем значение в список Redis.

        Args:
            value (str): значение для добавления в список.
        """
        self.list_storage.append(value)

    def retrieve(
        self,
    ) -> Iterator[str, ]:
        """Читаем все значения из списка Redis."""
        for _ in range(len(self.list_storage)):
            yield self.list_storage.pop(0)

    def current_batch_size(self) -> int:
        """Возращает размер батча в списке."""
        return len(self.list_storage)
