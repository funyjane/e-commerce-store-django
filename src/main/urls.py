from django.urls import path, include
from .views import *

app_name = "main"

urlpatterns = [
    path("", BaseListingListView.as_view(), name="listing-catalog"),
    path("<int:pk>/", BaseListingView.as_view(), name="listing-details"),
    path("items/", ItemListView.as_view(), name="item-catalog"),
    path("items/<int:pk>/", ItemView.as_view(), name="item-details"),
    path("cars/", CarListView.as_view(), name="car-catalog"),
    path("cars/<int:pk>/", CarView.as_view(), name="car-details"),
    path("services/", ServiceListView.as_view(), name="service-catalog"),
    path("services/<int:pk>/", ServiceView.as_view(), name="service-details"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("auth/seller/", SellerEditView.as_view(), name="seller-edit"),
]
