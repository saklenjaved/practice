from django.urls import path

from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('buy/<int:pk>/', views.buy_product, name='buy_product'),
    path('inventory/', views.dashboard, name='inventory_dashboard'),
    path('inventory/products/', views.product_list, name='product_list'),
    path('inventory/products/add/', views.add_product, name='add_product'),
    path('inventory/products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('inventory/products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('inventory/categories/', views.category_list, name='category_list'),
    path('inventory/categories/add/', views.category_add, name='category_add'),
    path('inventory/categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('inventory/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('inventory/purchases/', views.purchase_list, name='purchase_list'),
    path('inventory/purchases/add/', views.purchase_add, name='purchase_add'),
    path('inventory/sales/', views.sell_list, name='sell_list'),
    path('inventory/sales/add/', views.sell_add, name='sell_add'),
]
