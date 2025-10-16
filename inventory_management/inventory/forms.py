from django import forms
from .models import Product
from decimal import Decimal
from django.test import TestCase
from .models import Product
from decimal import Decimal

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
