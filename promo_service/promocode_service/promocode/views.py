from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CheckPromocodeSerializers
from .services import check_promocode


class GetCheckPromocodeView(APIView):
    """
    Класс для проверки промокода на валидность
    """

    parser_classes = [JSONParser]

    def get(self, request):
        promocode_request_data = CheckPromocodeSerializers(data=request.data)
        promocode_request_data.is_valid(raise_exception=True)
        res = check_promocode(
            promocode_value=promocode_request_data.data.get("promocode"),
            user_id=promocode_request_data.data.get("user_id"),
        )
        return Response(res)
