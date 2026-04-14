from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "expiration_date"]
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        }
