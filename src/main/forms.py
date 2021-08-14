from django import forms
from django.forms import ModelForm
from .models import AbstractBaseListing, Seller, Car, Item, Service, Tag


class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = "__all__"


class BaseListingForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all()
    )

    class Meta:
        model = AbstractBaseListing
        fields = "__all__"


class CarForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all()
    )

    class Meta:
        model = Car
        fields = "__all__"


class ItemForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all()
    )

    class Meta:
        model = Item
        fields = "__all__"


class ServiceForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all()
    )

    class Meta:
        model = Service
        fields = "__all__"
