from django.contrib import admin
from django.urls import include, path

import admin_panel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('admin_panel.api.urls'))
]
