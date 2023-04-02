from __future__ import annotations

import uuid
import pytz
from datetime import datetime

from rest_framework.response import Response
from .models import Promocode, PromocodeUserHistory, PromocodeType


def _is_promocode_valid(promo: Promocode):
    """Проверка промокода Promocode на валидность"""
    if not promo.is_valid:
        raise Exception("Promocode is not valid")


def _is_personal_promocode(promo: Promocode, user_id: uuid.UUID):
    """Проверка промокода Promocode на наличие конкретного пользователя для активации"""
    if promo.personal_user_id and promo.personal_user_id != user_id:
        raise Exception("It is personal promocode")


def _is_promocode_spoiled(promo: Promocode, time_zone):
    """Проверка промокода Promocode на срок годности"""
    if promo.activate_until >= datetime.now(tz=time_zone):
        return Exception("Promocode is spoiled")


def _get_promocode(promocode_value: str) -> Promocode | Exception:
    """Получение объекта Promocode через значение промокода promocode_value"""
    promocode_obj = Promocode.objects.filter(promo_value=promocode_value)
    if promocode_obj:
        return promocode_obj[0]
    else:
        raise Exception("Promocode is not found")


def _times_of_using_promocode(promocode_id: uuid.UUID) -> int:
    """Получение количества активаций промокода"""
    return PromocodeUserHistory.objects.filter(promocode_id=promocode_id).count()


def _get_max_number_of_activations(promocode_type_id: uuid.UUID) -> int:
    """Получение максимального числа активации промокода"""
    return PromocodeType.objects.filter(id=promocode_type_id)[0].max_number_activation


def _if_max_number_of_activations_exceed(promocode_id, promocode_type_id):
    """Проверка промокода Promocode на превышение максимального числа активаций """
    if _get_max_number_of_activations(promocode_type_id) < _times_of_using_promocode(promocode_id):
        raise Exception("Max number of activation exceed")


def check_promocode(promocode_value: str, user_id: uuid.UUID):
    promo = _get_promocode(promocode_value)
    _is_promocode_valid(promo)
    _is_personal_promocode(promo, user_id)
    _is_promocode_spoiled(promo, pytz.UTC)

    _if_max_number_of_activations_exceed(promo.id, promo.promocode_type_id.id)

    return Response({"status": "Valid promocode"})
