from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import *

app_name = "main"

urlpatterns = [
    path("", BaseListingListView.as_view(), name="listing-catalog"),
    path("<int:pk>/", BaseListingView.as_view(), name="listing-details"),
    path("listing/add/", BaseListingCreateView.as_view(), name="listing-create"),
    path(
        "listing/upd/<int:pk>",
        BaseListingUpdateView.as_view(),
        name="listing-update",
    ),
    path("items/", ItemListView.as_view(), name="item-catalog"),
    path("items/<int:pk>/", ItemView.as_view(), name="item-details"),
    path("items/add/", ItemCreateView.as_view(), name="item-create"),
    path(
        "items/upd/<int:pk>",
        ItemUpdateView.as_view(),
        name="item-update",
    ),
    path("cars/", CarListView.as_view(), name="car-catalog"),
    path("cars/<int:pk>/", CarView.as_view(), name="car-details"),
    path("cars/add/", CarCreateView.as_view(), name="car-create"),
    path(
        "cars/upd/<int:pk>",
        CarUpdateView.as_view(),
        name="car-update",
    ),
    path("services/", ServiceListView.as_view(), name="service-catalog"),
    path("services/<int:pk>/", ServiceView.as_view(), name="service-details"),
    path("services/add/", ServiceCreateView.as_view(), name="service-create"),
    path(
        "service/upd/<int:pk>",
        ServiceUpdateView.as_view(),
        name="service-update",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("auth/seller/", SellerEditView.as_view(), name="seller-edit"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
