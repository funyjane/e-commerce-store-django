import re
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.postgres.forms import SimpleArrayField

from main.models import AbstractBaseListing, Seller, Car, Item, Service, Picture


class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = "__all__"
        phone = PhoneNumberField()


class CustomSimpleArrayField(SimpleArrayField):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(",").strip()

    def validate(self, values):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(values)
        for tag in values:
            if not re.match(f"^[0-9a-zA-Z ]+$", tag):
                raise ValidationError(
                    _(
                        "Validation error! Use only alphanumeric "
                        + "symbols for tags and comma as delimiter!"
                    )
                )


class BaseListingForm(ModelForm):
    tags = CustomSimpleArrayField(forms.CharField(max_length=50), delimiter=",")
    phone = PhoneNumberField()

    class Meta:
        model = AbstractBaseListing
        fields = "__all__"


class CarForm(ModelForm):
    """This form is for creation and editing Car ads"""

    tags = CustomSimpleArrayField(forms.CharField(max_length=50), delimiter=",")

    class Meta:
        model = Car
        fields = "__all__"


class ItemForm(ModelForm):
    tags = CustomSimpleArrayField(forms.CharField(max_length=50), delimiter=",")

    class Meta:
        model = Item
        fields = "__all__"


class ServiceForm(ModelForm):
    tags = CustomSimpleArrayField(forms.CharField(max_length=50), delimiter=",")

    class Meta:
        model = Service
        fields = "__all__"


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ["img"]


PictureFormset = inlineformset_factory(Car, Picture, form=PictureForm, max_num=1)
