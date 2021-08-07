from django.views.generic import TemplateView, ListView, DetailView
from constance import config

from .models import AbstractBaseListing, Item, Car, Service, Tag


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
