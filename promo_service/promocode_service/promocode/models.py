import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class PromocodeType(models.Model):
    type_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField()
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    duration = models.PositiveIntegerField()  # ! Тут Integer это дней имеется в виду?

    class Meta:
        verbose_name = _('promocode type')
        verbose_name_plural = _('promocode type')


class Promocode(models.Model):
    promo_id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, )
    promo_value = models.CharField(_("promo value"), max_length=20, )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, )
    is_valid = models.BooleanField(_("is valid"), )
    is_reusable = models.BooleanField(_("is reusable"), )
    activate_until = models.DateTimeField(_("activate until"), )

    type_of_promocode = models.ForeignKey(PromocodeType,
                                          on_delete=models.CASCADE,
                                          verbose_name=_("type of promocode"), )

    class Meta:
        verbose_name = _('promocode')
        verbose_name_plural = _('promocodes')


class PromocodeUserHistory(models.Model):
    promo_id = models.ForeignKey(Promocode, on_delete=models.CASCADE)
    user_id = models.UUIDField()
    activated_at = models.DateTimeField(auto_now_add=True)  # при создании записи мы сразу активируем промокод
    expire_at = models.DateTimeField()  # Избыточность expiration - PromocodeType.duration

    class Meta:
        verbose_name = _('promocode history')
        verbose_name_plural = _('promocode history')
        constraints = [
            models.UniqueConstraint(fields=['promo_id', 'user_id'], name='unique pair promocode-user')
        ]
