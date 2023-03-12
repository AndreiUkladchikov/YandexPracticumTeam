from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_panel.rabbit_client import send_message
from admin_panel.models import MessageModel, MessageTypes


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
        message = MessageModel(
            type=get_type_by_sender("UGC"),
            subject=request.data['subject'],
            template='',
            user_id=request.data['user_id']
        )

        if 'film_id' in request.data.keys():
            message.film_id = request.data['film_id']

        return send_message(message)
