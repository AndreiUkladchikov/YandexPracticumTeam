from django.contrib import admin
from import_export.admin import ExportMixin
from rangefilter.filters import DateTimeRangeFilter, NumericRangeFilter

from .models import PromocodeUserHistory, Promocode, PromocodeType


@admin.register(Promocode)
class PromocodeAdmin(ExportMixin, admin.ModelAdmin):

    ordering = ('-created_at', )
    list_display = ('promo_value',
                    'type_of_promocode',
                    'is_valid',
                    'activate_until',
                    'created_at', )
    list_filter = ('is_valid',
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


@admin.register(PromocodeUserHistory)
class PromocodeUserHistoryAdmin(ExportMixin, admin.ModelAdmin):

    ordering = ('-activated_at', )
    list_display = ('promo_id',
                    'user_id',
                    'activated_at',
                    'expire_at', )
    list_filter = (('activated_at', DateTimeRangeFilter),
                   ('expire_at', DateTimeRangeFilter), )
    search_fields = ('user_id',
                     'promo_id__type_of_promocode__description',
                     'promo_id__promo_value', )
    list_display_links = ('promo_id',
                          'user_id', )
    raw_id_fields = ('promo_id', )

    list_per_page = 50


@admin.register(PromocodeType)
class PromocodeTypeAdmin(ExportMixin, admin.ModelAdmin):

    ordering = ('description', )
    list_display = ('description',
                    'discount',
                    'duration',
                    'max_number_activation', )
    list_filter = (('discount', NumericRangeFilter),
                   ('duration', NumericRangeFilter),
                   ('max_number_activation', NumericRangeFilter), )
    search_fields = ('description',
                     'discount',
                     'duration',
                     'max_number_activation', )
    list_display_links = ('description', )

    list_per_page = 50
