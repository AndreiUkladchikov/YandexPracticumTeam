from django.test import TestCase

from .tasks import create_promocodes


class TestTasks(TestCase):

    def test_create_promocodes_task(self):
        """Тестируем корректность настройки celery
        """
        assert create_promocodes.run(1)
        assert create_promocodes.run(2)
        assert create_promocodes.run(3)
