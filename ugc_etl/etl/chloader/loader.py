from typing import Iterable

from clickhouse_driver import Client

from common.config import settings


class ClickHouseLoader:
    """Загрузка данных батчами в ClickHouse."""

    host: str = settings.clickhouse_dsn

    def __init__(self) -> None:
        self.client = Client(self.host)

    def create_table(self) -> None:
        """Создаем таблицу, если она еще не была создана."""
        self.client.execute('CREATE TABLE IF NOT EXISTS film_watch (user_id UUID, film_id UUID, timestamp Int16)')

    def insert_batch(self, batch: Iterable[tuple, ]) -> int:
        """Загружаем данные пачкой в ClickHouse.

        Args:
            batch (Iterable[tuple, ]): батч для записи.

        Returns:
            int: количество вставленых строк.
        """
        return self.client.execute(
            'INSERT INTO film_watch (user_id, film_id, timestamp) VALUES',
            ((*values, ) for values in batch)
        )
