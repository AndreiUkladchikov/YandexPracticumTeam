from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from admin_panel.rabbit_client import send_message
from admin_panel.models import MessageTypes, PersonalizedTemplate, CommonTemplate

from admin_panel.api.serializers import NotificationSerializer


def get_type_by_sender(sender: str):
    # В зависимости от отправителя - выбираем определяем тип сообщения
    # Пока просто возвращаем рандомный тип (например UGC - уведомление о комментарии)
    return MessageTypes.UGC


class PersonalizedTemplateApiView(APIView):
    def get(self, request, *args, **kwargs):
        templates = PersonalizedTemplate.objects.filter(slug=kwargs['slug']).first()
        if templates is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(templates.template)


class CommonTemplateApiView(APIView):
    def get(self, request, *args, **kwargs):
        templates = CommonTemplate.objects.filter(slug=kwargs['slug']).first()
        if templates is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(templates.template)


class NotificationApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request, type=get_type_by_sender("UGC"))
        if serializer.is_valid():
            return send_message(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)