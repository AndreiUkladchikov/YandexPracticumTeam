from datetime import datetime, timedelta
from uuid import UUID, uuid4

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Task, Promocode, PromocodeType
from .tasks import notify_user


@receiver(post_save, sender=Task)
def generate_promocodes(sender, instance: Task, created: bool, **kwargs: dict):
    """Создаем промокоды для пользователей полученных по указанному users_api_endpoint
    и уведомляем пользователей о новом промокоде по notify_api_endpoint.
    """
    if created:
        users = get_users(instance.users_api_endpoint)

        for user_id in users:
            promocode = create_promocode(user_id, instance.promocode_type)
            notify_user.delay(user_id,
                              promocode.promo_value,
                              instance.notify_api_endpoint)

        instance.is_complete = True
        instance.save()


def get_users(users_api_endpoint: str):
    """Получаем по указаному адресу список идентификаторов пользователей 
    для которых необходимо сгенерировать персональные промокоды.
    """
    if not settings.DEBUG:
        resp = requests.get(users_api_endpoint)
        users = resp.json().get("users", [])
    else:
        users = [uuid4() for _ in range(100)]
    return users


def create_promocode(user_id: UUID, promocode_type: PromocodeType):
    """Создаем новый персональный промокод для пользователя.
    """
    new_promocode = Promocode.objects.create(
        personal_user_id=user_id,
        activate_until=datetime.now() + timedelta(days=promocode_type.duration),
        promocode_type_id=promocode_type.id,
    )
    return new_promocode
