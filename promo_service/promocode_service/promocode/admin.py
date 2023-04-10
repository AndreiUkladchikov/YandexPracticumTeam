from django.contrib import admin
from import_export.admin import ExportMixin
from rangefilter.filters import DateTimeRangeFilter, NumericRangeFilter

from .models import Promocode, PromocodeType, PromocodeUserHistory, Task


@admin.register(Promocode)
class PromocodeAdmin(ExportMixin, admin.ModelAdmin):
    ordering = ("-created_at",)
    list_display = (
        "promo_value",
        "promocode_type",
        "is_valid",
        "activate_until",
        "created_at",
    )
    list_filter = (
        "is_valid",
        ("promocode_type", admin.RelatedOnlyFieldListFilter),
        ("created_at", DateTimeRangeFilter),
        ("activate_until", DateTimeRangeFilter),
    )
    search_fields = (
        "promocode_type__description",
        "promocode_type__discount",
        "promocode_type__duration",
        "promo_value",
    )
    list_display_links = ("promo_value",)
    raw_id_fields = ("promocode_type",)

    list_per_page = 50


@admin.register(PromocodeUserHistory)
class PromocodeUserHistoryAdmin(ExportMixin, admin.ModelAdmin):
    ordering = ("-activated_at",)
    list_display = (
        "promocode",
        "user_id",
        "activated_at",
    )
    list_filter = (("activated_at", DateTimeRangeFilter),)
    search_fields = (
        "user_id",
        "promocode__promocode_type__description",
        "promocode__promo_value",
    )
    list_display_links = (
        "promocode",
        "user_id",
    )
    raw_id_fields = ("promocode",)
    list_per_page = 50


@admin.register(PromocodeType)
class PromocodeTypeAdmin(ExportMixin, admin.ModelAdmin):
    ordering = ("description",)
    list_display = (
        "description",
        "discount",
        "duration",
        "max_number_activation",
    )
    list_filter = (
        ("discount", NumericRangeFilter),
        ("duration", NumericRangeFilter),
        ("max_number_activation", NumericRangeFilter),
    )
    search_fields = (
        "description",
        "discount",
        "duration",
        "max_number_activation",
    )
    list_display_links = ("description",)

    list_per_page = 50


@admin.register(Task)
class TaskAdmin(ExportMixin, admin.ModelAdmin):
    ordering = ("description",)
    list_display = (
        "description",
        "is_complete",
        "promocode_type",
    )
    list_filter = (
        "is_complete",
        ("created_at", DateTimeRangeFilter),
    )
    search_fields = (
        "description",
        "users_api_endpoint",
        "notify_api_endpoint",
        "promocode_type__description",
    )
    list_display_links = ("description",)
    raw_id_fields = ("promocode_type",)

    list_per_page = 25
