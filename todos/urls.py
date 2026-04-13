from django.urls import path

from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/toggle/', views.toggle, name='toggle'),
    path('<int:pk>/delete/', views.delete_task, name='delete'),
]
