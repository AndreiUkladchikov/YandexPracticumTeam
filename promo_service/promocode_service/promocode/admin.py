from django.contrib import admin
from .models import PromocodeUserHistory, Promocode, PromocodeType

admin.site.register(Promocode)
admin.site.register(PromocodeUserHistory)
admin.site.register(PromocodeType)
