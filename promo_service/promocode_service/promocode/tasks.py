from uuid import UUID

import requests
from django.conf import settings
from celery import shared_task


@shared_task(
    name="notify_user",
    bind=True,
    ignore_result=True,
    acks_late=True,
    autoretry_for=(Exception,),
    max_retries=10,
    retry_backoff=True,
    retry_backoff_max=500,
    retry_jitter=True
)
def notify_user(user_id: UUID, promocode_value: str, notify_api_endpoint: str):
    """Отправляем уведомление пользователю о новом промокоде через сервис нотификации.
    """
    if not settings.DEBUG:
        payload = {'user_id': user_id, 'promocode': promocode_value}
        _ = requests.post(notify_api_endpoint, json=payload)
    else:
        pass
