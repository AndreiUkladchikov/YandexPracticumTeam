from django.urls import path

from admin_panel.api.v1 import views

urlpatterns = [
    path('person_templates/<slug>', views.PersonalizedTemplateApiView.as_view()),
    path('common_templates/<slug>', views.CommonTemplateApiView.as_view()),
    path('post_notificaton/', views.NotificationApiView.as_view())
]
