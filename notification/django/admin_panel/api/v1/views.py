from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from admin_panel.rabbit_client import send_message
from admin_panel.models import MessageModel, MessageTypes

from api.serializers import NotificationSerializer


def get_type_by_sender(sender: str):
    # В зависимости от отправителя - выбираем определяем тип сообщения
    # Пока просто возвращаем рандомный тип (например UGC - уведомление о комментарии)
    return MessageTypes.UGC


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
        serializer = NotificationSerializer(data=request, type=get_type_by_sender("UGC"))
        if serializer.is_valid():
            return send_message(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
