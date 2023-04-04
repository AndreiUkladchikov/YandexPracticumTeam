import time

from celery import shared_task


@shared_task
def create_promocodes(task_type):
    time.sleep(int(task_type) * 10)
    return True
