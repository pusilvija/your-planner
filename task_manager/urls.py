from django.urls import path

from . import views


urlpatterns = [
    path('api/taskboard/', views.TaskBoardView.as_view(), name='taskboard'),
    path('api/tasks/<int:id>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/<int:id>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('api/tasks/add-new-task/', views.AddTaskView.as_view(), name='add-new-task'),
    path('api/users/register/', views.RegisterView.as_view(), name='register'),
    path('api/users/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/tasks/', views.TasksPageView.as_view(), name='tasks-page'),
]
