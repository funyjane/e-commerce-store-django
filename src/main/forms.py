from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from main.models import AbstractBaseListing, Seller, Car, Item, Service, Tag, Picture


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


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ["img"]


PictureFormset = inlineformset_factory(Car, Picture, form=PictureForm, max_num=1)
