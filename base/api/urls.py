from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
    
    path('messages/', views.getMessages),
    path('message/<str:id>/', views.getMessage),
    path('create/<str:room_id>/', views.createMessage),
    path('<str:message_id>/delete/', views.deleteMessage)
]
