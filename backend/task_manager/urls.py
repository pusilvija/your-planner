from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_task, name='add_task'),
    path("tasks/delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("edit_task_name/<int:task_id>/", views.edit_task_name, name="edit_task_name"),
    path('task/<int:task_id>/', views.task_details, name='task_details'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('update-task-order/<int:task_id>/', views.update_task_order, name='update_task_order'),
]
