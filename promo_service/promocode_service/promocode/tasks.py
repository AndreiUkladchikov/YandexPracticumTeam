from __future__ import annotations

from datetime import timedelta
from uuid import UUID, uuid4

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Promocode, PromocodeType, Task


@shared_task(
    name="notify_user",
    bind=True,
    ignore_result=True,
    acks_late=True,
    autoretry_for=(Exception,),
    max_retries=10,
    retry_backoff=True,
    retry_backoff_max=500,
    retry_jitter=True,
)
def notify_user(user_id: UUID, promocode_value: str, notify_api_endpoint: str):
    """Отправляем уведомление пользователю о новом промокоде через сервис нотификации."""
    if not settings.DEBUG:
        payload = {"user_id": user_id, "promocode": promocode_value}
        _ = requests.post(notify_api_endpoint, json=payload)
    else:
        pass


@shared_task
def create_promocodes_task(task_id: UUID) -> None:
    """Создаем промокоды для пользователей полученных по указанному users_api_endpoint
    и уведомляем пользователей о новом промокоде по notify_api_endpoint.
    """
    task = Task.objects.get(id=task_id)

    users = get_users(task.users_api_endpoint)

    for user_id in users:
        promocode = create_promocode(user_id, task.promocode_type)
        notify_user.delay(user_id, promocode.promo_value, task.notify_api_endpoint)

    task.is_complete = True
    task.save()


def get_users(users_api_endpoint: str) -> list[str | UUID]:
    """Получаем по указаному адресу список идентификаторов пользователей
    для которых необходимо сгенерировать персональные промокоды.
    """
    if not settings.DEBUG:
        resp = requests.get(users_api_endpoint)
        users = resp.json().get("users", [])
    else:
        users = [uuid4() for _ in range(100)]
    return users


def create_promocode(user_id: UUID, promocode_type: PromocodeType) -> Promocode:
    """Создаем новый персональный промокод для пользователя."""
    new_promocode = Promocode.objects.create(
        is_valid=True,
        personal_user_id=user_id,
        activate_until=timezone.now() + timedelta(days=promocode_type.duration),
        promocode_type=promocode_type,
    )
    return new_promocode
