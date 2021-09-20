from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage


from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from django import forms
from ckeditor.widgets import CKEditorWidget
from sorl.thumbnail.admin import AdminImageMixin

from main.models import (
    Category,
    Seller,
    Subscriber,
    Item,
    Car,
    Service,
    ArchiveListing,
    SMSLog,
    Picture,
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


class PictureAdminInline(AdminImageMixin, admin.TabularInline):
    model = Picture


@admin.action(description="Archives selected listings")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Activate selected listings")
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.action(description="Mark lisitngs as sold")
def make_sold(modeladmin, request, queryset):
    queryset.update(sold=True)


@admin.action(description="Mark lisitngs as not sold")
def make_not_sold(modeladmin, request, queryset):
    queryset.update(is_sold=False)


class AdSubModelsAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "seller",
        "sold",
        "active",
    )
    ordering = ["created_at", "edited_at"]
    list_filter = (
        "sold",
        "active",
        "created_at",
        "edited_at",
    )
    inlines = [PictureAdminInline]
    search_fields = [
        "name",
        "seller__first_name",
        "seller__last_name",
        "seller__username",
    ]
    actions = [make_inactive, make_active, make_sold, make_not_sold]


admin.site.register(Seller)
admin.site.register(Car)
admin.site.register(Item)
admin.site.register(Service)
admin.site.register(ArchiveListing)
admin.site.register(Subscriber)
admin.site.register(SMSLog)
