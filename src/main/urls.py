from django.urls import path, re_path, include
from django.conf.urls.static import static
from .utils import trigger_error
from django.views.decorators.cache import cache_page
from django.conf import settings

from .views import *

cache_minutes_listview = 15
cache_minutes_detailview = 60
app_name = "main"

urlpatterns = [

    path("sentry-debug/", trigger_error),
    re_path(r"^search/[.]*$", (SearchView.as_view()), name="search"),
    path(
        "all/",
        cache_page(60 * cache_minutes_listview)(BaseListingListView.as_view()),
        name="listing-catalog",
    ),
    path(
        "<int:pk>/",
        cache_page(60 * cache_minutes_detailview)(BaseListingView.as_view()),
        name="listing-details",
    ),
    path("listing/add/", BaseListingCreateView.as_view(), name="listing-create"),
    path(
        "listing/upd/<int:pk>",
        BaseListingUpdateView.as_view(),
        name="listing-update",
    ),
    path(
        "items/",
        cache_page(60 * cache_minutes_listview)(ItemListView.as_view()),
        name="item-catalog",
    ),
    path(
        "items/<int:pk>/",
        cache_page(60 * cache_minutes_detailview)(ItemView.as_view()),
        name="item-details",
    ),
    path("items/add/", ItemCreateView.as_view(), name="item-create"),
    path(
        "items/upd/<int:pk>",
        ItemUpdateView.as_view(),
        name="item-update",
    ),
    path(
        "cars/",
        cache_page(60 * cache_minutes_listview)(CarListView.as_view()),
        name="car-catalog",
    ),
    path(
        "cars/<int:pk>/",
        CarView.as_view(),
        name="car-details",
    ),
    path("cars/add/", CarCreateView.as_view(), name="car-create"),
    path(
        "cars/upd/<int:pk>",
        CarUpdateView.as_view(),
        name="car-update",
    ),
    path(
        "services/",
        cache_page(60 * cache_minutes_listview)(ServiceListView.as_view()),
        name="service-catalog",
    ),
    path(
        "services/<int:pk>/",
        cache_page(60 * cache_minutes_detailview)(ServiceView.as_view()),
        name="service-details",
    ),
    path("services/add/", ServiceCreateView.as_view(), name="service-create"),
    path(
        "service/upd/<int:pk>",
        ServiceUpdateView.as_view(),
        name="service-update",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/seller/", SellerEditView.as_view(), name="seller-edit"),
    path("accounts/profile/", UserEditView.as_view(), name="user-edit"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
