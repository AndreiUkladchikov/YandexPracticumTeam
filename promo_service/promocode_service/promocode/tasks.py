from __future__ import annotations

from datetime import timedelta
from uuid import UUID, uuid4

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .logger import logger
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
def notify_user(self, user_id: UUID, promocode_value: str, notify_api_endpoint: str):
    """We send a notification to the user about a new promotional code through the notification service."""
    if not settings.DEBUG:
        logger.debug(f"Start send message to user {user_id} with promocode {promocode_value}")
        payload = {"user_id": user_id, "promocode": promocode_value}
        _ = requests.post(notify_api_endpoint, json=payload)
        logger.debug(f"Message send to user {user_id} with promocode {promocode_value}")
    else:
        logger.debug(f"Message send to user {user_id} with promocode {promocode_value}")
        pass


@shared_task
def create_promocodes_task(task_id: UUID) -> None:
    """Create promotional codes for users received by the specified users_api_endpoint
    and notify users about a new promotional code by notify_api_endpoint.
    """
    task = Task.objects.get(id=task_id)

    users = get_users(task.users_api_endpoint)

    for user_id in users:
        promocode = create_promocode(user_id, task.promocode_type)
        notify_user.delay(user_id, promocode.promo_value, task.notify_api_endpoint)

    task.is_complete = True
    task.save()
    logger.debug(f"Task {task.id} complete and save")


def get_users(users_api_endpoint: str) -> list[str | UUID]:
    """We get a list of user IDs at the specified address
    for which it is necessary to generate personal promotional codes.
    """
    if not settings.DEBUG:
        logger.debug(f"Start get users id list from url {users_api_endpoint}")
        resp = requests.get(users_api_endpoint)
        users = resp.json().get("users", [])
        logger.debug(f"Get users id list from url {users_api_endpoint} complete")
    else:
        users = [uuid4() for _ in range(100)]
        logger.debug(f"Get test users id list from url {users_api_endpoint}")
    return users


def create_promocode(user_id: UUID, promocode_type: PromocodeType) -> Promocode:
    """We create a new personal promotional code for the user."""
    logger.debug(f"Start create promocode {promocode_type.description} for user {user_id}")
    new_promocode = Promocode.objects.create(
        is_valid=True,
        personal_user_id=user_id,
        activate_until=timezone.now() + timedelta(days=promocode_type.duration),
        promocode_type=promocode_type,
    )
    logger.debug(f"Promocode {promocode_type.description} for user {user_id} created")
    return new_promocode
