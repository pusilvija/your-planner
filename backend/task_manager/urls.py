from django.urls import path

from . import views
from django.urls import path


urlpatterns = [
    path('api/taskboard/', views.TaskBoardView.as_view(), name='taskboard'),
    path('api/tasks/<int:id>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/<int:id>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('api/tasks/add-new-task/', views.AddTaskView.as_view(), name='add-new-task'),
]
