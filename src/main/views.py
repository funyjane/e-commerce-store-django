from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from constance import config

from .models import AbstractBaseListing, Item, Car, Service, Tag, Seller, Picture
from .forms import (
    SellerForm,
    BaseListingForm,
    CarForm,
    ItemForm,
    ServiceForm,
    PictureFormset,
)


class IndexPageView(TemplateView):
    template_name = "pages/index.html"
    turn_on_block = config.MAINTENANCE_MODE


class BaseListingListView(ListView):
    template_name = "main/listing_list.html"
    model = AbstractBaseListing
    paginate_by = 10

    def get_queryset(self):
        tag_filter = self.request.GET.get("tag")
        if tag_filter:
            new_context = AbstractBaseListing.objects.filter(
                tags=Tag.objects.get(title=tag_filter)
            )
        else:
            new_context = AbstractBaseListing.objects.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super(BaseListingListView, self).get_context_data(**kwargs)
        context["tag"] = self.request.GET.get("tag")
        return context


class BaseListingView(DetailView):
    template_name = "main/listing_details.html"
    model = AbstractBaseListing


class BaseListingCreateView(CreateView):

    model = AbstractBaseListing
    form_class = BaseListingForm
    template_name = "main/listing_create.html"

    def get_success_url(self):
        return reverse("main:listing-update", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        if self.request.user.groups.filter(name="banned users").exists():
            raise PermissionDenied(_("Ops, you have been banned, you cannot post!"))
        else:
            return super().form_valid(form)


class BaseListingUpdateView(UpdateView):

    model = AbstractBaseListing
    form_class = BaseListingForm
    template_name = "main/listing_update.html"

    def get_success_url(self):
        return reverse("main:listing-update", kwargs={"pk": self.object.pk})


class ItemListView(ListView):
    template_name = "main/item_list.html"
    model = Item
    paginate_by = 10

    def get_queryset(self):
        tag_filter = self.request.GET.get("tag")
        if tag_filter:
            new_context = Item.objects.filter(tags=Tag.objects.get(title=tag_filter))
        else:
            new_context = Item.objects.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context["tag"] = self.request.GET.get("tag")
        return context


class ItemView(DetailView):
    template_name = "main/item_details.html"
    model = Item


class ItemCreateView(BaseListingCreateView):
    model = Item
    form_class = ItemForm

    def get_success_url(self):
        return reverse("main:item-update", kwargs={"pk": self.object.pk})


class ItemUpdateView(BaseListingUpdateView):
    model = Item
    form_class = ItemForm

    def get_success_url(self):
        return reverse("main:item-update", kwargs={"pk": self.object.pk})


class CarListView(ListView):
    template_name = "main/car_list.html"
    model = Car
    paginate_by = 10

    def get_queryset(self):
        tag_filter = self.request.GET.get("tag")
        if tag_filter:
            new_context = Car.objects.filter(tags=Tag.objects.get(title=tag_filter))
        else:
            new_context = Car.objects.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        context["tag"] = self.request.GET.get("tag")
        return context


class CarView(DetailView):
    template_name = "main/car_details.html"
    model = Car

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            img = Picture.objects.filter(car=self.get_object()).last()
        except:
            img = None
        data["picture"] = img
        return data


class CarCreateView(LoginRequiredMixin, BaseListingCreateView):
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse("main:car-update", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["picture_forms"] = PictureFormset()
        return context

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller
        advert_form = form.save(commit=False)
        formset = PictureFormset(
            self.request.POST, self.request.FILES, instance=advert_form
        )
        if formset.is_valid():
            formset.instance = form.save()
            formset.save()
            return super(CarCreateView, self).form_valid(form)
        else:
            return self.render_to_response({"form": form, "picture_forms": formset})


class CarUpdateView(LoginRequiredMixin, BaseListingUpdateView):
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse("main:car-update", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["picture_forms"] = PictureFormset()
        return context

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller
        advert_form = form.save(commit=False)
        formset = PictureFormset(
            self.request.POST, self.request.FILES, instance=advert_form
        )
        if formset.is_valid():
            formset.instance = form.save()
            formset.save()
            return super(CarUpdateView, self).form_valid(form)
        else:
            return self.render_to_response({"form": form, "picture_forms": formset})


class ServiceListView(ListView):
    template_name = "main/service_list.html"
    model = Service
    paginate_by = 10

    def get_queryset(self):
        tag_filter = self.request.GET.get("tag")
        if tag_filter:
            new_context = Service.objects.filter(tags=Tag.objects.get(title=tag_filter))
        else:
            new_context = Service.objects.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        context["tag"] = self.request.GET.get("tag")
        return context


class ServiceView(DetailView):
    template_name = "main/service_details.html"
    model = Service


class ServiceCreateView(LoginRequiredMixin, BaseListingCreateView):
    model = Service
    form_class = ServiceForm

    def get_success_url(self):
        return reverse("main:service-update", kwargs={"pk": self.object.pk})


class ServiceUpdateView(LoginRequiredMixin, BaseListingUpdateView):
    model = Service
    form_class = ServiceForm

    def get_success_url(self):
        return reverse("main:service-update", kwargs={"pk": self.object.pk})


class SellerEditView(LoginRequiredMixin, UpdateView):
    """editing Seller"""

    model = Seller
    form_class = SellerForm
    success_url = reverse_lazy("main:seller-edit")
    template_name = "main/accounts/seller_edit.html"

    def get_object(self, queryset=None):
        user = self.request.user.id
        return get_object_or_404(Seller, id=user)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "main/accounts/user_edit.html"
    success_url = reverse_lazy("main:user-edit")

    fields = ("email", "first_name", "last_name")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if "email" in form.changed_data:

            email = form.cleaned_data.get("email")
            user = self.request.user
            socialaccount = user.socialaccount_set.filter(user=user).first()
            if socialaccount is not None:
                if socialaccount.extra_data.get("email") != email:
                    messages.error(self.request, "Email is invalid")
                    return self.form_invalid(form)

            messages.success(self.request, "Email successfully updated")
            return super().form_valid(form)
        else:
            messages.success(self.request, "Email successfully updated")
            return super().form_valid(form)
