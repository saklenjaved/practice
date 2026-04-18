from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import Category, Product, Purchase, Sell


class BuyProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='Quantity',
        widget=forms.NumberInput(attrs={'min': 1}),
    )

    def __init__(self, *args, max_stock=None, **kwargs):
        self.max_stock = max_stock
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if self.max_stock is not None and qty > self.max_stock:
            raise ValidationError(f'Only {self.max_stock} available in stock.')
        return qty


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].validators.append(MinValueValidator(0))
        self.fields['price'].validators.append(MinValueValidator(Decimal('0')))


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'quantity', 'price', 'buyer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].validators.append(MinValueValidator(1))
        self.fields['price'].validators.append(MinValueValidator(Decimal('0')))
        self.fields['price'].help_text = 'Cost per unit for this purchase.'


class SellForm(forms.ModelForm):
    class Meta:
        model = Sell
        fields = ['product', 'quantity', 'price', 'customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].validators.append(MinValueValidator(1))
        self.fields['price'].validators.append(MinValueValidator(Decimal('0')))
        self.fields['price'].help_text = 'Sale price per unit.'
