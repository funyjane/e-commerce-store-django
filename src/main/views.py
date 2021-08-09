from django.views.generic import TemplateView, ListView, DetailView
from constance import config

from .models import AbstractBaseListing, Item, Car, Service


class IndexPageView(TemplateView):
    template_name = "pages/index.html"
    turn_on_block = config.MAINTENANCE_MODE


class BaseListingListView(ListView):
    template_name = "main/listing_list.html"
    model = AbstractBaseListing


class BaseListingView(DetailView):
    template_name = "main/listing_details.html"
    model = AbstractBaseListing


class ItemListView(ListView):
    template_name = "main/item_list.html"
    model = Item


class ItemView(DetailView):
    template_name = "main/item_details.html"
    model = Item


class CarListView(ListView):
    template_name = "main/car_list.html"
    model = Car


class CarView(DetailView):
    template_name = "main/car_details.html"
    model = Car


class ServiceListView(ListView):
    template_name = "main/service_list.html"
    model = Service


class ServiceView(DetailView):
    template_name = "main/service_details.html"
    model = Service
