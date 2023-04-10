from django.urls import path

from . import views

urlpatterns = [
    path(
        "check_promocode",
        views.CheckPromocodeView.as_view(),
        name="Check promocode view",
    ),
    path(
        "apply_promocode",
        views.ApplyPromocodeView.as_view(),
        name="Apply promocode view",
    ),
    path("user_history", views.UserHistoryView.as_view(), name="User history view"),
]
