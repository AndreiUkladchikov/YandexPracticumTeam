import json
from datetime import datetime, timedelta

import pytz
from django.test import TestCase
from rest_framework import status

from .models import Promocode, PromocodeType, Task
from .tasks import create_promocodes_task


test_promo_type = {
    "description": "Test promocode type",
    "discount": 100,
    "duration": 30,
    "max_number_activation": 5,
}
test_task_template = {
    'description': 'Test task',
    'users_api_endpoint': 'http://test.route.loc/',
    'notify_api_endpoint': 'http://test.route.loc/',
}
promo_value = "QWERTY"

user_id = "2d82814e-3d96-4bed-b4b1-940738144181"

data = {"user_id": user_id, "promocode": promo_value}

history_data = {"user_id": user_id}


class TestCheckPromocode(TestCase):
    """Tests for check promocode route."""

    def setUp(self) -> None:
        promo_type_obj = PromocodeType.objects.create(**test_promo_type)
        Promocode.objects.create(
            is_valid=True,
            promo_value=promo_value,
            activate_until=datetime.now(tz=pytz.UTC) + timedelta(days=30),
            promocode_type_id=promo_type_obj,
        )

    def test_check_promocode(self):
        res = self.client.get("/api/v1/check_promocode", data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestApplyPromocode(TestCase):
    """Tests for apply promocode route."""

    def setUp(self) -> None:
        promo_type_obj = PromocodeType.objects.create(**test_promo_type)
        Promocode.objects.create(
            is_valid=True,
            promo_value=promo_value,
            activate_until=datetime.now(tz=pytz.UTC) + timedelta(days=30),
            promocode_type_id=promo_type_obj,
        )

    def test_apply_promocode(self):
        res = self.client.post(
            "/api/v1/apply_promocode",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestPromocodeHistory(TestCase):
    """Tests for promocode history."""

    def setUp(self) -> None:
        promo_type_obj = PromocodeType.objects.create(**test_promo_type)
        Promocode.objects.create(
            is_valid=True,
            promo_value=promo_value,
            activate_until=datetime.now(tz=pytz.UTC) + timedelta(days=30),
            promocode_type_id=promo_type_obj,
        )
        self.client.post(
            "/api/v1/apply_promocode",
            data=json.dumps(data),
            content_type="application/json",
        )

    def test_get_promocode_history(self):
        res = self.client.get("/api/v1/user_history", data=history_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestTasks(TestCase):

    def test_create_promocodes_task(self):
        """Testing the correctness of the celery settings."""
        promocode_type = PromocodeType.objects.create(
            **test_promo_type
        )
        test_task = Task.objects.create(
            promocode_type=promocode_type,
            **test_task_template
        )

        assert create_promocodes_task.run(test_task.id)
