from abc import ABC

from rest_framework import serializers

from .models import Promocode, PromocodeUserHistory


class PromocodeValidateSerializers(serializers.Serializer):
    user_id = serializers.UUIDField()
    promocode = serializers.CharField()


class HistoryValidateSerializers(serializers.Serializer):
    user_id = serializers.UUIDField()


class PromocodeSerializer(serializers.StringRelatedField, ABC):
    class Meta:
        model = Promocode
        fields = ("promo_value",)


class PromocodeHistorySerializer(serializers.ModelSerializer):
    promocode_id = PromocodeSerializer()

    class Meta:
        model = PromocodeUserHistory
        fields = (
            "promocode_id",
            "activated_at",
        )
