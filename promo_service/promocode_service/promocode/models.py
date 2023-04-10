import random
import uuid

from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


def get_promo_code(num_chars=8) -> str:
    """Function for generation promo code

    :param num_chars: number of characters (default 8)

    :return: promo code
    """
    code_chars = "123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    code = ""
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start : slice_start + 1]
    return code


class PromocodeType(models.Model):
    """Тип промокода, описывающий его основные характеристики

    Prop:
        id: uuid идентификатор типа промокода
        description: str краткое описание
        discount: int процент скидки (допустимое значение от 1 до 100)
        duration: int кол-во дней, в течении которых можно воспользоваться промоколом
        max_number_activation: int максимальное кол-во раз, которое пользователь
                                   может воспользоваться промоколом (если 0 то неограничено)
    """

    id = models.UUIDField(
        _("type id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    description = models.TextField(
        _("description"),
    )
    discount = models.IntegerField(
        _("discount"),
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    duration = models.PositiveIntegerField(
        _("duration"),
    )
    max_number_activation = models.PositiveIntegerField(
        _("max number activation"),
        default=0,
    )

    def __str__(self):
        return self.description

    class Meta:
        db_table = "promocode_type"
        verbose_name = _("promocode type")
        verbose_name_plural = _("promocode type")


class Task(models.Model):
    """Задания на создание персональных промокодов

    Prop:
        id: uuid идентификатор задания
        description: str краткое описание задания
        created_at: datetime метка времени, когда задание было создано
        users_api_endpoint: str url-адрес ручки сервиса, которая вернет перечень id пользователей,
                                для которых необходимо создать промокоды (например, можно из сервиса
                                статистики получить сто самых активных комментаторов или ревьюеров фильмов)
        notify_api_endpoint: str url-адрес ручки сервиса нотификации, которая уведомит пользователя
                                 о новом промокоде
        is_complete: bool текущий статус задания (True если задание выполнено и созданы промокоды)
        promocode_type: uuid внешний ключ указывающий на тип промокода
                                (размер скидки, период действия в днях,
                                кол-во активаций для пользователя)
    """

    id = models.UUIDField(
        _("type id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    description = models.TextField(
        _("description"),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    users_api_endpoint = models.URLField(
        _("users api endpoint"),
    )
    notify_api_endpoint = models.URLField(
        _("notify api endpoint"),
    )
    is_complete = models.BooleanField(
        _("is complete"),
        default=False,
        editable=False,
    )

    promocode_type = models.ForeignKey(
        PromocodeType,
        on_delete=models.CASCADE,
        verbose_name=_("type of promocode"),
    )

    def __str__(self) -> str:
        return self.description

    class Meta:
        db_table = "task"
        verbose_name = _("task")
        verbose_name_plural = _("tasks")


class Promocode(models.Model):
    """Промокоды

    Prop:
        id: uuid идентификатор промокода
        promo_value: str случайное значение из 8 символов для промокода
        created_at: str метка времени, когда был создан промокод
        is_valid: bool ?????
        number_activations: int сколько раз воспользовались промокодом
        personal_user_id: uuid идентификатор пользователя (указывается если промокод персональный)
        activate_until: datetime дата, по которую возможно воспользоваться промокодом
        promocode_type: uuid идентификатор типа промокода
    """

    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    promo_value = models.CharField(
        _("promo value"),
        max_length=20,
        validators=[MinLengthValidator(8)],
        default=get_promo_code,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    is_valid = models.BooleanField(
        _("is valid"),
    )
    personal_user_id = models.UUIDField(
        _("personal user id"),
        blank=True,
        null=True,
    )
    activate_until = models.DateTimeField(
        _("activate until"),
    )

    promocode_type = models.ForeignKey(
        PromocodeType,
        on_delete=models.CASCADE,
        verbose_name=_("type of promocode"),
    )

    def __str__(self):
        return self.promo_value

    class Meta:
        db_table = "promocode"
        verbose_name = _("promocode")
        verbose_name_plural = _("promocodes")


class PromocodeUserHistory(models.Model):
    """История использования промокодов пользователями

    Prop:
        promocode: uuid идентификатор промокода
        user_id: uuid идентификатор пользователя
        activated_at: datetime метка времени, когда был использован промокод
                               (при создании записи мы сразу ее ставим)
    """

    promocode_id = models.ForeignKey(
        Promocode,
        on_delete=models.CASCADE,
        verbose_name=_("promo id"),
    )
    user_id = models.UUIDField(
        _("user id"),
    )
    activated_at = models.DateTimeField(
        _("activated at"),
        auto_now_add=True,
    )

    class Meta:
        db_table = "promocode_user_history"
        verbose_name = _("promocode history")
        verbose_name_plural = _("promocode history")
        constraints = [
            models.UniqueConstraint(
                fields=["promocode_id", "user_id"], name="unique pair promocode-user"
            )
        ]
