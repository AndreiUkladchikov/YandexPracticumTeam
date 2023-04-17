from __future__ import annotations

import uuid
from datetime import datetime

import pytz

from .custom_exceptions import (
    ItIsPersonalPromocode,
    MaxNumberOfActivationExceed,
    PromocodeAlreadyActivatedByCurrentUser,
    PromocodeIsNotFound,
    PromocodeIsNotValid,
    PromocodeIsSpoiled,
    UserIsNotInUserHistory,
)
from .models import Promocode, PromocodeType, PromocodeUserHistory


class PromocodeService:
    def __init__(self, promocode: Promocode):
        self.promocode = promocode

    def _is_promocode_valid(self):
        """Проверка промокода Promocode на валидность"""
        if not self.promocode.is_valid:
            raise PromocodeIsNotValid(promocode_id=self.promocode.id)

    def _is_personal_promocode(self, user_id: uuid.UUID):
        """Проверка промокода Promocode на наличие конкретного пользователя для активации"""
        if (
            self.promocode.personal_user_id
            and self.promocode.personal_user_id != user_id
        ):
            raise ItIsPersonalPromocode(promocode_id=self.promocode.id)

    def _is_promocode_spoiled(self, time_zone: pytz.utc):
        """Проверка промокода Promocode на срок годности"""
        if self.promocode.activate_until <= datetime.now(tz=time_zone):
            raise PromocodeIsSpoiled(promocode_id=self.promocode.id)

    def _times_of_using_promocode(self) -> int:
        """Получение количества активаций промокода"""
        return PromocodeUserHistory.objects.filter(
            promocode_id=self.promocode.id
        ).count()

    def _get_max_number_of_activations(self) -> int:
        """Получение максимального числа активации промокода"""
        return PromocodeType.objects.filter(id=self.promocode.promocode_type.id)[
            0
        ].max_number_activation

    def _if_max_number_of_activations_exceed(self):
        """Проверка промокода Promocode на превышение максимального числа активаций"""
        if self._get_max_number_of_activations() < self._times_of_using_promocode():
            raise MaxNumberOfActivationExceed(promocode_id=self.promocode.id)

    def _if_promocode_already_activated_by_current_user(self, user_id: uuid.UUID):
        if PromocodeUserHistory.objects.filter(
            promocode_id=self.promocode.id, user_id=user_id
        ):
            raise PromocodeAlreadyActivatedByCurrentUser(
                promo_id=self.promocode, user_id=user_id
            )

    def _add_to_history(self, user_id: uuid.UUID):
        p = PromocodeUserHistory(promocode_id=self.promocode, user_id=user_id)
        p.save()

    def verify(self, user_id: uuid.UUID):
        self._is_promocode_valid()
        self._is_personal_promocode(user_id)
        self._is_promocode_spoiled(pytz.UTC)

        self._if_promocode_already_activated_by_current_user(user_id)

        self._if_max_number_of_activations_exceed()

    def apply(self, user_id: uuid.UUID):
        self.verify(user_id)
        self._add_to_history(user_id)


def _get_promocode(promocode_value: str) -> Promocode | Exception:
    """Получение объекта Promocode через значение промокода promocode_value"""
    promocode_obj = Promocode.objects.filter(promo_value=promocode_value)
    if promocode_obj:
        return promocode_obj[0]
    else:
        raise PromocodeIsNotFound(promo_value=promocode_value)


def check_promocode(promocode_value: str, user_id: uuid.UUID):
    """Функция проверки промокода"""
    promo = _get_promocode(promocode_value)
    service = PromocodeService(promocode=promo)
    service.verify(user_id)

    return {"status": "Valid promocode"}


def apply_promocode(promocode_value: str, user_id: uuid.UUID):
    promo = _get_promocode(promocode_value)
    service = PromocodeService(promocode=promo)
    service.apply(user_id)

    return {"status": "Promo code applied successfully"}


def get_user_history(user_id: uuid.UUID):
    user_history = PromocodeUserHistory.objects.filter(user_id=user_id)
    if not user_history:
        raise UserIsNotInUserHistory(user_id)
    return user_history
