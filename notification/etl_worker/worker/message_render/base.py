import abc
from uuid import UUID


class BaseMessageRender(abc.ABC):

    @abc.abstractmethod
    def get_template(self) -> None:
        """Получаем шаблон и id пользователя из очереди."""
        pass

    @abc.abstractmethod
    def get_user_info(self,
                      item_id: UUID) -> None:
        """Получаем информацию о пользователе или фильме по указаному URL."""
        pass

    @abc.abstractmethod
    def render_message(self,
                       template: str,
                       user_info: dict[str, str]) -> str:
        """Рендерим сообщение в соответствии с контекстом."""
        pass

    @abc.abstractmethod
    def send_message(self) -> int:
        """Добавляем сформирование сообщение в очередь на отправку."""
        pass
