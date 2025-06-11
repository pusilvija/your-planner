from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("task_manager.urls")),
    path("api/", include("task_manager.urls")),
    path('admin/', admin.site.urls),
]
