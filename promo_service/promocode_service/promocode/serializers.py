
from rest_framework import serializers

from .models import Promocode


class PromocodeTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promocode
        fields = ('promo_id', 'promo_value', 'type_of_promocode', 'is_valid', 'activate_until',)


class CheckPromocodeSerializers(serializers.Serializer):
    user_id = serializers.UUIDField()
    promocode = serializers.CharField()
