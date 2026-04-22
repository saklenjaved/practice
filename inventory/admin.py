from django.contrib import admin
from .models import User, UserProfile, Category, Product, Purchase, Sell, Cart

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)

admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'address')
    search_fields = ('user__username', 'phone')
    
admin.site.register(UserProfile ,UserProfileAdmin) 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    
admin.site.register(Product, ProductAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'buyer')
    search_fields = ('product__name', 'buyer')
    list_filter = ('date',)
    
admin.site.register(Purchase, PurchaseAdmin)

class SellAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'customer')
    search_fields = ('product__name', 'customer__username')
    list_filter = ('date',)

admin.site.register(Sell, SellAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    search_fields = ('user__username',)
    list_filter = ('added_at',)
    
admin.site.register(Cart, CartAdmin)