from urllib.parse import urlencode

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.models import User

from .forms import BuyProductForm, CategoryForm, ProductForm, PurchaseForm, SellForm
from .models import Category, Product, Purchase, Sell


def _resolve_user(request):
    uid = request.session.get('user_id')
    if not uid:
        return None
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist:
        request.session.flush()
        return None


def _login_redirect(request):
    q = urlencode({'next': request.get_full_path()})
    return redirect(f"{reverse('login')}?{q}")


def _shop_audience(user):
    if user is None:
        return 'guest'
    if user.role == 'admin':
        return 'admin'
    return 'user'


def shop(request):
    products = Product.objects.select_related('category').all().order_by('name')
    user = _resolve_user(request)
    return render(
        request,
        'inventory/shop.html',
        {
            'products': products,
            'shop_audience': _shop_audience(user),
        },
    )


def buy_product(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        pk=pk,
    )
    user = _resolve_user(request)
    if user is None:
        return _login_redirect(request)

    if user.role == 'admin':
        messages.info(
            request,
            'As an admin, record customer sales under Inventory → Sales (Record sale).',
        )
        return redirect('sell_add')

    if product.quantity <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('shop')

    if request.method == 'POST':
        form = BuyProductForm(request.POST, max_stock=product.quantity)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            with transaction.atomic():
                locked = Product.objects.select_for_update().get(pk=product.pk)
                if locked.quantity < qty:
                    form.add_error(
                        'quantity',
                        f'Only {locked.quantity} left in stock.',
                    )
                else:
                    Sell.objects.create(
                        product=locked,
                        quantity=qty,
                        price=locked.price,
                        customer=user,
                    )
                    locked.quantity -= qty
                    locked.save(update_fields=['quantity'])
                    messages.success(
                        request,
                        f'Purchased {qty} × {locked.name} at {locked.price} each.',
                    )
                    return redirect('shop')
    else:
        form = BuyProductForm(max_stock=product.quantity)

    return render(
        request,
        'inventory/buy.html',
        {'product': product, 'form': form},
    )


def _require_login(request):
    user = _resolve_user(request)
    if not user:
        return None, _login_redirect(request)
    return user, None


def _require_admin(request):
    user, redirect_resp = _require_login(request)
    if redirect_resp:
        return None, redirect_resp
    if user.role != 'admin':
        return None, redirect('user_dashboard')
    return user, None


def dashboard(request):
    _, resp = _require_admin(request)
    if resp:
        return resp

    products = Product.objects.all()
    categories = Category.objects.all()
    purchases = Purchase.objects.select_related('product', 'buyer').order_by('-id')[:5]
    sells = Sell.objects.select_related('product', 'customer').order_by('-id')[:5]
    low_stock = products.filter(quantity__lt=5, quantity__gte=0)

    return render(
        request,
        'inventory/dashboard.html',
        {
            'product_count': products.count(),
            'category_count': categories.count(),
            'purchase_count': Purchase.objects.count(),
            'sell_count': Sell.objects.count(),
            'purchases': purchases,
            'sells': sells,
            'low_stock': low_stock,
        },
    )


def product_list(request):
    user = _resolve_user(request)
    if user is not None and user.role != 'admin':
        return redirect('shop')

    products = Product.objects.select_related('category').all()
    return render(request, 'inventory/product_list.html', {'products': products})


def add_product(request):
    user, resp = _require_admin(request)
    if resp:
        return resp
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product created.')
        return redirect('product_list')
    return render(
        request,
        'inventory/product_form.html',
        {'form': form, 'form_title': 'Add product'},
    )


def edit_product(request, pk):
    user, resp = _require_admin(request)
    if resp:
        return resp
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product updated.')
        return redirect('product_list')
    return render(
        request,
        'inventory/product_form.html',
        {'form': form, 'form_title': 'Edit product', 'product': product},
    )


def delete_product(request, pk):
    user, resp = _require_admin(request)
    if resp:
        return resp
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


def category_list(request):
    user, resp = _require_admin(request)
    if resp:
        return resp
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})


def category_add(request):
    user, resp = _require_admin(request)
    if resp:
        return resp
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category created.')
        return redirect('category_list')
    return render(request, 'inventory/category_form.html', {'form': form, 'form_title': 'Add category'})


def category_edit(request, pk):
    user, resp = _require_admin(request)
    if resp:
        return resp
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category updated.')
        return redirect('category_list')
    return render(
        request,
        'inventory/category_form.html',
        {'form': form, 'form_title': 'Edit category', 'category': category},
    )


def category_delete(request, pk):
    user, resp = _require_admin(request)
    if resp:
        return resp
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('category_list')
    return render(request, 'inventory/category_confirm_delete.html', {'category': category})


def purchase_list(request):
    user, resp = _require_admin(request)
    if resp:
        return resp
    purchases = Purchase.objects.select_related('product', 'buyer').order_by('-id')
    return render(request, 'inventory/purchase_list.html', {'purchases': purchases})


def purchase_add(request):
    user, resp = _require_admin(request)
    if resp:
        return resp
    form = PurchaseForm(request.POST or None)
    if form.is_valid():
        with transaction.atomic():
            product = Product.objects.select_for_update().get(
                pk=form.cleaned_data['product'].pk,
            )
            purchase = form.save()
            product.quantity += purchase.quantity
            product.save(update_fields=['quantity'])
        messages.success(request, 'Purchase recorded and stock updated.')
        return redirect('purchase_list')
    return render(request, 'inventory/purchase_form.html', {'form': form})


def sell_list(request):
    user, resp = _require_admin(request)
    if resp:
        return resp
    sells = Sell.objects.select_related('product', 'customer').order_by('-id')
    return render(request, 'inventory/sell_list.html', {'sells': sells})


def sell_add(request):
    user, resp = _require_admin(request)
    if resp:
        return resp
    form = SellForm(request.POST or None)
    if form.is_valid():
        product = form.cleaned_data['product']
        qty = form.cleaned_data['quantity']
        with transaction.atomic():
            locked = Product.objects.select_for_update().get(pk=product.pk)
            if locked.quantity < qty:
                form.add_error(
                    'quantity',
                    f'Not enough stock (available: {locked.quantity}).',
                )
            else:
                sell = form.save()
                locked.quantity -= sell.quantity
                locked.save(update_fields=['quantity'])
                messages.success(request, 'Sale recorded and stock updated.')
                return redirect('sell_list')
    return render(request, 'inventory/sell_form.html', {'form': form})
