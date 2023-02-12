from typing import Any, Generator

from clickhouse_driver import Client
from common.config import settings


class ClickHouseLoader:
    """Загрузка данных батчами в ClickHouse."""

    host: str = settings.clickhouse_host

    def __init__(self) -> None:
        self.client = Client(host=self.host)

    def create_table(self) -> None:
        """Создаем таблицу, если она еще не была создана."""
        self.client.execute(
            "CREATE TABLE IF NOT EXISTS film_watch (user_id UUID, film_id UUID, timestamp Int16) ENGINE = MergeTree() ORDER BY (user_id, film_id)"
        )

    def insert_batch(self, batch: Generator[tuple[str, str, int], Any, None]) -> int:
        """Загружаем данные пачкой в ClickHouse.

        Args:
            batch (Generator[tuple, ]): батч для записи.

        Returns:
            int: количество вставленных строк.
        """
        return self.client.execute(
            "INSERT INTO film_watch (user_id, film_id, timestamp) VALUES",
            ((*values,) for values in batch),
        )
