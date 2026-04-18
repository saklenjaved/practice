from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/register/', views.register, name='register'),
    # path('accounts/profile/', views.profile, name='profile'),
    path('accounts/user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('accounts/admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]

