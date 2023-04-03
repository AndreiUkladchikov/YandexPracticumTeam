from __future__ import annotations

import uuid
from datetime import datetime

import custom_exceptions
import pytz

from .models import Promocode, PromocodeType, PromocodeUserHistory


def _is_promocode_valid(promo: Promocode):
    """Проверка промокода Promocode на валидность"""
    if not promo.is_valid:
        raise custom_exceptions.PromocodeIsNotValid


def _is_personal_promocode(promo: Promocode, user_id: uuid.UUID):
    """Проверка промокода Promocode на наличие конкретного пользователя для активации"""
    if promo.personal_user_id and promo.personal_user_id != user_id:
        raise custom_exceptions.ItIsPersonalPromocode


def _is_promocode_spoiled(promo: Promocode, time_zone: pytz.utc):
    """Проверка промокода Promocode на срок годности"""
    if promo.activate_until >= datetime.now(tz=time_zone):
        return custom_exceptions.PromocodeIsSpoiled


def _get_promocode(promocode_value: str) -> Promocode | Exception:
    """Получение объекта Promocode через значение промокода promocode_value"""
    promocode_obj = Promocode.objects.filter(promo_value=promocode_value)
    if promocode_obj:
        return promocode_obj[0]
    else:
        raise custom_exceptions.PromocodeIsNotFound


def _times_of_using_promocode(promocode_id: uuid.UUID) -> int:
    """Получение количества активаций промокода"""
    return PromocodeUserHistory.objects.filter(promocode_id=promocode_id).count()


def _get_max_number_of_activations(promocode_type_id: uuid.UUID) -> int:
    """Получение максимального числа активации промокода"""
    return PromocodeType.objects.filter(id=promocode_type_id)[0].max_number_activation


def _if_max_number_of_activations_exceed(promocode_id, promocode_type_id):
    """Проверка промокода Promocode на превышение максимального числа активаций"""
    if _get_max_number_of_activations(promocode_type_id) < _times_of_using_promocode(
        promocode_id
    ):
        raise custom_exceptions.MaxNumberOfActivationExceed


def check_promocode(promocode_value: str, user_id: uuid.UUID):
    promo = _get_promocode(promocode_value)
    _is_promocode_valid(promo)
    _is_personal_promocode(promo, user_id)
    _is_promocode_spoiled(promo, pytz.UTC)

    _if_max_number_of_activations_exceed(promo.id, promo.promocode_type_id.id)

    return {"status": "Valid promocode"}
