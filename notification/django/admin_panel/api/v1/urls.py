from django.urls import path

from admin_panel.api.v1 import views

urlpatterns = [
    path('templates/<uuid:pk>', views.TemplateApiView.as_view()),
    path('post_notificaton/', views.NotificationApiView.as_view())
]
