from django.shortcuts import render, redirect
from django.db.models import Sum, Count, Min
from .models import User, UserProfile, Category, Product, Purchase, Sell, Cart
from .forms import UserForm, LoginForm, UserProfileForm, CategoryForm, ProductForm, PurchaseForm, SellForm, CartForm
# Create your views here.


def register(request):
    if request.method == 'GET':
        userform = UserForm()
        userprofile_form = UserProfileForm()
        return render(request, 'register.html', {'userform': userform, 'userprofile_form': userprofile_form})
    elif request.method == 'POST':
        userform = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        
        if userform.is_valid() and userprofile_form.is_valid():
            user = userform.save()
            userprofile  = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            return redirect('login')
        return render(request, 'register.html', {'userform': userform, 'userprofile_form': userprofile_form})
        

def login(request):
    if request.method == 'GET':
        loginform = LoginForm()
        return render(request, 'login.html', {'loginform': loginform})
    
    elif request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            try:
                user = User.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                request.session['role'] = user.role
                
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                return redirect('home')
            except User.DoesNotExist:
                return render(request, 'login.html', {'loginform': loginform})

def logout(request):
    request.session.flush()
    return redirect('home') 

def home(request):
    product = Product.objects.filter(stock__gt=0).values('id','name', 'category__name').annotate(total_stock=Sum('stock'), price=Min('price'))
    # categories = Category.objects.all()
    return render(request, 'home.html', {'product': product})

def admin_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    if user.role != 'admin':
        return redirect('home')
    
    categories_count = Category.objects.count()
    products_count = Product.objects.count()
    purchase_count = Purchase.objects.count()
    sell_count = Sell.objects.count()
    total_stock = Product.objects.aggregate(total=Sum('stock'))['total']
    
    return render(request, 'admin_dashboard.html', {'categories_count': categories_count,
        'products_count': products_count, 'purchase_count': purchase_count,
        'sell_count': sell_count, 'total_stock': total_stock,
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    user = User.objects.get(id=user_id)
    if user.role != 'admin':
        return redirect('home')
        
    if request.method == 'GET':
        category_form = CategoryForm()
        return render(request, 'add_category.html', {'category_form': category_form})
        
    elif request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('admin_dashboard')
        return render(request, 'add_category.html', {'category_form': category_form})
      
def update_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'GET':
        update_category = CategoryForm(instance=category)
        return render(request, 'update_category.html', {'update_category': update_category})
    
    elif request.method == 'POST':
        update_category = CategoryForm(request.POST, instance=category)
        if update_category.is_valid():
            update_category.save()
            return redirect('category_list')
        return render(request, 'update_category.html', {'update_category': update_category})

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_list')

def product_list(request):
    products = Product.objects.values('id','name', 'category__name', 'price', 'stock').distinct()
    return render(request, 'product_list.html', {'products': products})

def add_product(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    user = User.objects.get(id=user_id)
    if user.role != 'admin':
        return redirect('home')
    
    if request.method == 'GET':
        add_product = ProductForm()
        return render(request, 'add_product.html', {'add_product': add_product})
    
    elif request.method == 'POST':
        add_product = ProductForm(request.POST)
    if add_product.is_valid():
        name = add_product.cleaned_data['name']
        category = add_product.cleaned_data['category']
        price = add_product.cleaned_data['price']
        stock = add_product.cleaned_data['stock']

        existing_product = Product.objects.filter(name=name, category=category).first()

        if existing_product:
            existing_product.stock += stock
            existing_product.price = price  # optional: update price
            existing_product.save()
        else:
            add_product.save()

        return redirect('product_list')

    return render(request, 'add_product.html', {'add_product': add_product})
        
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'GET':
        update_product = ProductForm(instance=product)
        return render(request, 'update_product.html', {'update_product': update_product})
    
    elif request.method == 'POST':
        update_product = ProductForm(request.POST, instance=product)
        if update_product.is_valid():
            update_product.save()
            return redirect('product_list')
        return render(request, 'update_product.html', {'update_product': update_product})
        
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_list')


def purchase(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    if not user.role == 'admin':
        return redirect('home')
    
    if request.method == 'GET':
        purchase_form = PurchaseForm()
        return render(request, 'purchase.html', {'purchase_form': purchase_form})
    
    elif request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)
        if purchase_form.is_valid():
            purchase = purchase_form.save(commit=False)
            purchase.buyer = user
            purchase.save()

            product = purchase.product            
            product.stock = int(product.stock) + int(purchase.quantity)
            product.save()
            
            return redirect('purchase_list')
        return render(request, 'purchase.html', {'purchase_form': purchase_form})
        
def purchase_list(request):
    purchases = Purchase.objects.select_related('product', 'buyer').all()
    for p in purchases:
        p.total_amount = p.price * p.quantity
    return render(request, 'purchase_list.html', {'purchases': purchases})
        

def add_to_cart(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)

    cart_item = Cart.objects.filter(user_id=user.id, product_id=product.id).first()

    if request.method == 'POST':
        form = CartForm(request.POST)

        if form.is_valid():
            qty = form.cleaned_data['quantity']

            if cart_item:
                cart_item.quantity += qty
                cart_item.save()
            else:
                Cart.objects.create(
                    user=user,
                    product=product,
                    quantity=qty
                )

            return redirect('cart')

    else:
        form = CartForm()

    return render(request, 'add_to_cart.html', {
        'form': form,
        'product': product
    })

def cart(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # ✅ return added

    user = User.objects.get(id=user_id)

    cart_items = Cart.objects.select_related('product').filter(user_id=user.id)

    print(str(cart_items.query))

    total = 0

    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
    

def update_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart_item)

        if form.is_valid():
            form.save()
            return redirect('cart')

    else:
        form = CartForm(instance=cart_item)

    return render(request, 'update_cart.html', {'form': form})

def delete_cart(request, cart_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        cart_item = Cart.objects.get(id=cart_id, user_id=user_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart')


def buy(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    cart_items = Cart.objects.select_related('product').filter(user_id=user.id)

    total = 0

    for item in cart_items:
        product = item.product

        # 🔥 ONLY DECREASE
        if item.quantity <= product.stock:
            product.stock -= item.quantity
            product.save()

            Sell.objects.create(
                customer=user,
                product=product,
                quantity=item.quantity,
                price=product.price
            )

            total += product.price * item.quantity

    cart_items.delete()

    return render(request, 'buy_success.html', {'total': total})


def sell(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    if user.role != 'admin':
        return redirect('home')

    if request.method == 'POST':
        form = SellForm(request.POST)

        if form.is_valid():
            sell = form.save(commit=False)

            product = sell.product

            if sell.quantity > product.stock:
                return redirect('sell')

            product.stock -= sell.quantity
            product.save()

            sell.customer = user
            sell.save()

            return redirect('sell_list')

    else:
        form = SellForm()

    return render(request, 'sell.html', {'form': form})

def sell_list(request):
    sells = Sell.objects.select_related('product', 'customer').all().order_by('-date')

    print(str(sells.query))
    
    grand_total = 0   # 🔥 new

    for s in sells:
        s.total = float(s.quantity) * float(s.price)
        grand_total += s.total   # 🔥 add each total

    return render(request, 'sell_list.html', {
        'sells': sells,
        'grand_total': grand_total   # 🔥 pass to template
    })