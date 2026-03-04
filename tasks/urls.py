from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/<int:task_id>/toggle-complete/', views.toggle_complete, name='toggle_complete'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]
