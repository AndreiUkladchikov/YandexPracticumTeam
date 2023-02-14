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
