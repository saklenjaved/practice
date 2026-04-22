Inventory Management System

This is Inventory Management System project built using Django.
This project supportd two roles:

1. Admin - Manages products, categories, purchases and sell
2. User - Show products, add to cart and buy items

Models:
1. User - stores user info and role admin/user
2. UserProfile - user details linked with user
3. Category - group products(e.g., T-Shirts, Pants)
4. Product - stores name, category, price, stock
5. Purchase - represents stocks comin IN, when admin purchases
6. Sell - represents stocks going OUT, when user buys products
7. Cart - temparory storage before user buying

Features :
Admin Feature
* add/update/delete categories
* add/update/delete products
* manage purchases
* manage sells
* In Admin Dashboard
  - Total Products
  - Total Stock
  - Total Categories
  - Total Purchases
  - Total Sells

User Features
* View Available Products
* Register & Login
* Add products to cart
* update/delete cart items
* Buy products
  
