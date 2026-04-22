from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    
    path('category_list/', views.category_list, name="category_list"),
    path('add-category/', views.add_category, name="add_category"),
    path('update-category/<int:category_id>/', views.update_category, name="update_category"),
    path('delete-category/<int:category_id>/', views.delete_category, name="delete_category"),
    
    
    path('product_list/', views.product_list, name="product_list"),
    path('add-product/', views.add_product, name="add_product"),
    path('update-product/<int:product_id>/', views.update_product, name="update_product"),
    path('delete-product/<int:product_id>/', views.delete_product, name="delete_product"),

    path('purchase/', views.purchase, name="purchase"),
    path('purchase_list/', views.purchase_list, name="purchase_list"),    
    
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:cart_id>/', views.delete_cart, name='delete_cart'),
    
    path('buy/', views.buy, name='buy'),
    
    path('sell/', views.sell, name='sell'),
    path('sell-list/', views.sell_list, name='sell_list'),
    
]

