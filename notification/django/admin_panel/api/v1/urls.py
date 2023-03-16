from django.urls import path

from admin_panel.api.v1 import views

urlpatterns = [
    path('person_templates/<slug>', views.PersonalizedTemplateApiView.as_view(), name='person_templates'),
    path('common_templates/<slug>', views.CommonTemplateApiView.as_view(), name='common_templates'),
    path('post_notificaton/', views.NotificationApiView.as_view(), name='post_notification')
]
