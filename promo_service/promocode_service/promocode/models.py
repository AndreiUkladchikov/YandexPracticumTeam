import uuid
import random
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _


def get_promo_code(num_chars=8) -> str:
    """
    Function for generation promo code
    :param num_chars: number of characters (default 8)
    :return: promo code
    """
    code_chars = '123456789ABCDEFGHIJKLMNPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


class PromocodeType(models.Model):
    type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    duration = models.PositiveIntegerField()
    max_number_activation = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.description

    class Meta:
        db_table = "promocode_type"
        verbose_name = _('promocode type')
        verbose_name_plural = _('promocode type')


class Promocode(models.Model):
    promo_id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    promo_value = models.CharField(_("promo value"), max_length=20,
                                   validators=[MinLengthValidator(8)], default=get_promo_code)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    is_valid = models.BooleanField(_("is valid"), )
    number_activations = models.PositiveIntegerField(default=0, editable=False)
    personal_user_id = models.UUIDField(blank=True, null=True)
    activate_until = models.DateTimeField(_("activate until"), )

    type_of_promocode = models.ForeignKey(PromocodeType,
                                          on_delete=models.CASCADE,
                                          verbose_name=_("type of promocode"), )

    class Meta:
        db_table = "promocode"
        verbose_name = _('promocode')
        verbose_name_plural = _('promocodes')


class PromocodeUserHistory(models.Model):
    promo_id = models.ForeignKey(Promocode, on_delete=models.CASCADE)
    user_id = models.UUIDField()
    activated_at = models.DateTimeField(auto_now_add=True)  # при создании записи мы сразу активируем промокод
    expire_at = models.DateTimeField()

    class Meta:
        db_table = "promocode_user_history"
        verbose_name = _('promocode history')
        verbose_name_plural = _('promocode history')
        constraints = [
            models.UniqueConstraint(fields=['promo_id', 'user_id'], name='unique pair promocode-user')
        ]