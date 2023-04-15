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
    """Function for generation promo code.

    :param num_chars: number of characters (default 8)

    :return: promo code
    """
    code_chars = "123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    code = ""
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


class PromocodeType(models.Model):
    """Type of promocode, describe promocode main properties.

    Prop:
        id: uuid promocode type id
        description: str short description of promocode
        discount: int persent of discount
        duration: int count days that promocode is valid
        max_number_activation: int the maximum number of times 
                                   that the promotional code can be activated
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
    """Task for create personal promocodes.

    Prop:
        id: uuid task id
        description: str task short description
        created_at: datetime when task was created
        users_api_endpoint: str service handle url that will return a list of user ids,
                                for which you need to create promotional codes (for example, you can from the service
                                statistics to get the 100 most active movie commentators or reviewers)
        notify_api_endpoint: str url address of the notification service handle that will notify the user
                                 about the new promo code
        is_complete: bool current status of the task (True if the task is completed and promo codes have been created)
        promocode_type: uuid foreign key indicating the type of promotional code
                             (discount amount, validity period in days,
                             number of activations per user)
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
    """Promocodes model.

    Prop:
        id: uuid promocode id
        promo_value: str random value of 8 characters for the promo code
        created_at: str timestamp when the promo code was generated
        is_valid: bool promocode state
        number_activations: int how many times did use this promo code
        personal_user_id: uuid user ID (indicated if the promotional code is personal)
        activate_until: datetime date by which the promo code can be used
        promocode_type: uuid promo code type identifier
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
    """History of using promo codes by users.

    Prop:
        promocode: uuid promocode id
        user_id: uuid user id
        activated_at: datetime timestamp when the promo code was used
                               (when creating a record, we immediately put it)
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
