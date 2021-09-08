from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import (
    User,
    Car,
    Item,
    Service,
    Category,
    Tag,
    Seller,
)
from main.factories import (
    SellerFactory,
    CarFactory,
    ServiceFactory,
    ItemFactory,
    CategoryFactory,
    TagFactory,
    PictureFactory,
)
from main.utils import download_image_from_url

TESTS_QTY = 10


class Command(BaseCommand):
    help = "Generates test data"
    cars = []

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Poppulating testing database...")

        for _ in range(TESTS_QTY):
            CategoryFactory()

        for _ in range(TESTS_QTY):
            TagFactory()

        for _ in range(TESTS_QTY):
            SellerFactory()

        for _ in range(TESTS_QTY):
            self.cars += [CarFactory()]

        for _ in range(TESTS_QTY):
            ItemFactory()

        for _ in range(TESTS_QTY):
            ServiceFactory()

        for car_ad in self.cars:
            PictureFactory(
                car=car_ad,
                pic="uploads/car_pics/"
                + download_image_from_url("https://picsum.photos/700/500"),
            )

        self.stdout.write("Done poppulating database")
