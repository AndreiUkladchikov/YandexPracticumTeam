from http import HTTPStatus

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase

from admin_panel.models import PersonalizedTemplate, CommonTemplate


class PersonTemplateTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('admin_panel/api/v1', include('admin_panel.api.v1.urls')),
    ]

    def setUp(self) -> None:
        PersonalizedTemplate.objects.create(slug='Person1')

    def test_api(self):
        """
        Персональный темплейт для пользователя
        """
        url = reverse('person_templates', kwargs={'slug':'Person1'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CommonTemplateTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('admin_panel/api/v1', include('admin_panel.api.v1.urls')),
    ]

    def setUp(self) -> None:
        CommonTemplate.objects.create(slug='Common1')

    def test_api(self):
        """
        Шаблон массовой рассылки
        """
        url = reverse('common_templates', kwargs={'slug':'Common1'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class NotificationSerializationTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('admin_panel/api/v1', include('admin_panel.api.v1.urls')),
    ]

    def test_api(self):
        """
        Проверяем работу NotificationApiView
        """
        url = reverse('post_notification')
        response = self.client.post(url, format='json', data={})
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
