from django.urls import path

from . import views
from django.urls import path


urlpatterns = [
    path('api/taskboard/', views.TaskBoardView.as_view(), name='taskboard'),
]
