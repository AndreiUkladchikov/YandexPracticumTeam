import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PromocodeType(models.Model):
    type_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField()
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    duration = models.PositiveIntegerField()


class Promocode(models.Model):
    promo_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    promo_value = models.CharField(max_length=20)
    type_of_promocode = models.ForeignKey(PromocodeType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField()
    is_reusable = models.BooleanField()
    activate_until = models.DateTimeField()


class PromocodeUserHistory(models.Model):
    promo_id = models.ForeignKey(Promocode, on_delete=models.CASCADE)
    user_id = models.UUIDField()
    activated_at = models.DateTimeField(auto_now_add=True)  # при создании записи мы сразу активируем промокод
    expire_at = models.DateTimeField()  # Избыточность expiration - PromocodeType.duration

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['promo_id', 'user_id'], name='unique pair promocode-user')
        ]
