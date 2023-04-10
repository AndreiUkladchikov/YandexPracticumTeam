from django.http import JsonResponse
from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .custom_exceptions import PromocodeException
from .serializers import (
    HistoryValidateSerializers,
    PromocodeHistorySerializer,
    PromocodeValidateSerializers,
)
from .services import apply_promocode, check_promocode, get_user_history


class BaseView(APIView):
    """Базовый класс для всех Views, который обрабатывает исключения"""

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)

        except PromocodeException as e:
            logger.exception(e)
            return self._response(
                {"error": e.__str__()}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(e)
            return self._response(
                data={"error": "Something went wrong!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=status.HTTP_200_OK):
        return JsonResponse(
            data,
            status=status,
        )


class CheckPromocodeView(BaseView):
    """
    Класс для проверки промокода на валидность
    """

    def get(self, request):
        promocode_request_data = PromocodeValidateSerializers(data=request.GET)
        promocode_request_data.is_valid(raise_exception=True)
        res = check_promocode(
            promocode_value=promocode_request_data.data.get("promocode"),
            user_id=promocode_request_data.data.get("user_id"),
        )
        return JsonResponse(res)


class ApplyPromocodeView(BaseView):
    """
    Класс для применения промокода
    """

    def post(self, request):
        promocode_request_data = PromocodeValidateSerializers(data=request.data)
        promocode_request_data.is_valid(raise_exception=True)

        promocode_value = promocode_request_data.data.get("promocode")
        user_id = promocode_request_data.data.get("user_id")

        res = apply_promocode(promocode_value, user_id)

        return JsonResponse(res)


class UserHistoryView(BaseView):
    """
    Класс для просмотра истории примененных промокодов
    """

    def get(self, request):
        request_data = HistoryValidateSerializers(data=request.GET)
        request_data.is_valid(raise_exception=True)

        history = get_user_history(request_data.data.get("user_id"))

        serializer = PromocodeHistorySerializer(instance=history, many=True)

        return Response(serializer.data)
