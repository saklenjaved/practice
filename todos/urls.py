from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('update_category/<int:category_id>', views.update_category, name="update_category"),
    path('delete_category/<int:category_id>', views.delete_category, name="delete_category"),
    path('todo_by_category/<int:category_id>', views.todo_by_category, name="todo_by_category"),
    path('done/', views.done_tasks, name="done_tasks"),
    path('update_task/<int:task_id>', views.update_task, name="update_task"),
    path('delete_task/<int:task_id>', views.delete_task, name="delete_task"),
    
]

