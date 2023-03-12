from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import pika

from admin_panel.config import settings


class TemplateApiView(APIView):
    def get_queryset(self):
        # Получаем шаблоны
        return []

    def get(self, request, *args, **kwargs):
        templates = self.get_queryset()
        # Some logic
        return JsonResponse({})


class NotificationApiView(APIView):
    def post(self, request, *args, **kwargs):
        cred = pika.PlainCredentials(settings.send_queue_username, settings.send_queue_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.send_queue_host, credentials=cred))
        channel = connection.channel()

        channel.queue_declare(queue='test-queue')

        channel.basic_publish('',
                              'test-queue',
                              request.data,)
        connection.close()
        return JsonResponse({})
