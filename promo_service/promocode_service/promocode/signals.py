from django.db.models.signals import post_save
from django.dispatch import receiver

from .logger import logger
from .models import Task
from .tasks import create_promocodes_task


@receiver(post_save, sender=Task)
def generate_promocodes(sender, instance: Task, created: bool, **kwargs: dict) -> None:
    """Create promotional codes for users received by the specified users_api_endpoint
    and notify users about a new promotional code by notify_api_endpoint.
    """
    if created:
        logger.debug('Task %s start.', instance.id)
        create_promocodes_task.delay(instance.id)
