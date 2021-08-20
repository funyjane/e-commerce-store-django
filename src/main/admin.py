from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage


from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from django import forms
from ckeditor.widgets import CKEditorWidget

from main.models import (
    Category,
    Seller,
    Subscriber,
    Tag,
    Item,
    Car,
    Service,
    ArchiveListing,
)


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        fields = "__all__"
        model = FlatPage


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = [
        "title",
    ]
    list_display = [
        "title",
    ]


admin.site.register(Seller)
admin.site.register(Car)
admin.site.register(Item)
admin.site.register(Service)
admin.site.register(ArchiveListing)
admin.site.register(Subscriber)
