from rest_framework import status

from loguru import logger

from rest_framework.views import APIView
from django.http import JsonResponse

from .serializers import CheckPromocodeSerializers
from .services import check_promocode


JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


class BaseView(APIView):
    """Базовый класс для всех Views, который обрабатывает исключения"""

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.info(f"{e.__str__()}")
            return self._response({'error': e.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=status.HTTP_200_OK):
        return JsonResponse(data,
                            status=status,
                            )


class GetCheckPromocodeView(BaseView):
    """
    Класс для проверки промокода на валидность
    """

    def get(self, request):
        promocode_request_data = CheckPromocodeSerializers(data=request.data)
        promocode_request_data.is_valid(raise_exception=True)
        res = check_promocode(
            promocode_value=promocode_request_data.data.get("promocode"),
            user_id=promocode_request_data.data.get("user_id"),
        )
        return JsonResponse(res)
