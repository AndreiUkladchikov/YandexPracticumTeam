from django.urls import path

from . import views

urlpatterns = [
    path("check_promo", views.GetCheckPromocodeView.as_view(), name='Check promocode view'),
]
