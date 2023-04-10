from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task
from .tasks import create_promocodes_task


@receiver(post_save, sender=Task)
def generate_promocodes(sender, instance: Task, created: bool, **kwargs: dict) -> None:
    """Создаем промокоды для пользователей полученных по указанному users_api_endpoint
    и уведомляем пользователей о новом промокоде по notify_api_endpoint.
    """
    if created:
        create_promocodes_task.delay(instance.id)
