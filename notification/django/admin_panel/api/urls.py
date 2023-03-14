from django.urls import include, path

import admin_panel

urlpatterns = [
    path('v1/', include('admin_panel.api.v1.urls'))
]
