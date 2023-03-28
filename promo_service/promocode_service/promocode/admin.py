from django.contrib import admin
from import_export.admin import ExportMixin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

from .models import PromocodeUserHistory, Promocode, PromocodeType


@admin.register(Promocode)
class PromocodeAdmin(ExportMixin, admin.ModelAdmin):

    ordering = ('-created_at', )
    list_display = ('promo_value',
                    'type_of_promocode',
                    'is_valid',
                    'is_reusable',
                    'activate_until',
                    'created_at', )
    list_filter = ('is_valid',
                   'is_reusable',
                   ('type_of_promocode', admin.RelatedOnlyFieldListFilter),
                   ('created_at', DateTimeRangeFilter),
                   ('activate_until', DateTimeRangeFilter), )
    search_fields = ('type_of_promocode__description',
                     'type_of_promocode__discount',
                     'type_of_promocode__duration',
                     'promo_value', )
    list_display_links = ('promo_value', )
    raw_id_fields = ('type_of_promocode', )

    list_per_page = 50


admin.site.register(PromocodeUserHistory)
admin.site.register(PromocodeType)
