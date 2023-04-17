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
from .logger import logger
from .models import Promocode, PromocodeType, PromocodeUserHistory


class PromocodeService:
    def __init__(self, promocode: Promocode):
        self.promocode = promocode

    def _is_promocode_valid(self):
        """Checking the Promocode for validity."""
        logger.debug(f"Validate promocode {self}: {self.__dict__}")
        if not self.promocode.is_valid:
            raise PromocodeIsNotValid(promocode_id=self.promocode.id)

    def _is_personal_promocode(self, user_id: uuid.UUID):
        """Checking the Promocode for a specific user for activation."""
        logger.debug(f"Check personal promocode {self}: {self.__dict__}")
        if (
            self.promocode.personal_user_id
            and self.promocode.personal_user_id != user_id
        ):
            raise ItIsPersonalPromocode(promocode_id=self.promocode.id)

    def _is_promocode_spoiled(self, time_zone: pytz.utc):
        """Checking the Promocode for the expiration date."""
        logger.debug(f"Checking the promocode expiration date {self}: {self.__dict__}")
        if self.promocode.activate_until <= datetime.now(tz=time_zone):
            raise PromocodeIsSpoiled(promocode_id=self.promocode.id)

    def _times_of_using_promocode(self) -> int:
        """Getting the count of promotional code activations."""
        logger.debug(f"Getting the count of promocode activations {self}: {self.__dict__}")
        return PromocodeUserHistory.objects.filter(
            promocode_id=self.promocode.id
        ).count()

    def _get_max_number_of_activations(self) -> int:
        """Getting the maximum activation count of the promotional code."""
        logger.debug(f"Getting the maximum activation count {self}: {self.__dict__}")
        return PromocodeType.objects.filter(id=self.promocode.promocode_type_id.id)[
            0
        ].max_number_activation

    def _if_max_number_of_activations_exceed(self):
        """Checking the Promocode for exceeding the maximum count of activations."""
        logger.debug(f"Checking the promocode for exceeding the maximum count of activations {self}: {self.__dict__}")
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
        """Add promocode activate info to history."""
        logger.debug(f"Add promocode activate info to history {self}: {self.__dict__}")
        p = PromocodeUserHistory(promocode_id=self.promocode, user_id=user_id)
        p.save()

    def verify(self, user_id: uuid.UUID):
        """Verify promocode."""
        logger.debug(f"Verify promocode {self}: {self.__dict__}")
        self._is_promocode_valid()
        self._is_personal_promocode(user_id)
        self._is_promocode_spoiled(pytz.UTC)

        self._if_promocode_already_activated_by_current_user(user_id)

        self._if_max_number_of_activations_exceed()

    def apply(self, user_id: uuid.UUID):
        """Apply promocode."""
        logger.debug(f"Apply promocode {self}: {self.__dict__}")
        self.verify(user_id)
        self._add_to_history(user_id)


def _get_promocode(promocode_value: str) -> Promocode | Exception:
    """Getting the Promocode object via promocode_value."""
    logger.debug(f"Get promocode {promocode_value}")
    promocode_obj = Promocode.objects.filter(promo_value=promocode_value)
    if promocode_obj:
        return promocode_obj[0]
    else:
        raise PromocodeIsNotFound(promo_value=promocode_value)


def check_promocode(promocode_value: str, user_id: uuid.UUID):
    """Promo code verification function."""
    logger.debug(f"Check promocode {promocode_value} for user {user_id}")
    promo = _get_promocode(promocode_value)
    service = PromocodeService(promocode=promo)
    service.verify(user_id)

    return {"status": "Valid promocode"}


def apply_promocode(promocode_value: str, user_id: uuid.UUID):
    """Apply promocode by user."""
    logger.debug(f"Apply promocode {promocode_value} for user {user_id}")
    promo = _get_promocode(promocode_value)
    service = PromocodeService(promocode=promo)
    service.apply(user_id)

    return {"status": "Promo code applied successfully"}


def get_user_history(user_id: uuid.UUID):
    """Get user promocode history."""
    logger.debug(f"Get history for user {user_id}")
    user_history = PromocodeUserHistory.objects.filter(user_id=user_id)
    if not user_history:
        raise UserIsNotInUserHistory(user_id)
    return user_history
