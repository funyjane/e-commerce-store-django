from django import forms
from django.forms import ModelForm
from .models import Seller


class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = ["first_name", "last_name", "email", "code_inn"]
