import factory
import random

from factory.django import DjangoModelFactory
from django.conf import settings
from main.utils import download_image_from_url, inn_gen, generate_phone
from main.models import (
    Seller,
    AbstractBaseListing,
    Category,
    Car,
    Service,
    Item,
    Tag,
    Picture,
)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker("sentence", nb_words=3)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.Faker(
        "word",
    )


class SellerFactory(DjangoModelFactory):
    class Meta:
        model = Seller

    username = factory.Faker("user_name")
    code_inn = inn_gen()
    email = factory.Faker("ascii_safe_email")
    # phone_number = generate_phone()
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=10)
    category = factory.SubFactory(CategoryFactory)
    seller = factory.SubFactory(SellerFactory)
    type_of = factory.Faker("sentence", nb_words=2)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            rnd = random.randint(1, 4)
            for i in range(min(rnd, len(extracted))):
                tag = extracted[random.randint(0, len(extracted) - 1)]
                self.tags.add(tag)


class CarFactory(DjangoModelFactory):
    class Meta:
        model = Car

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=10)
    category = factory.SubFactory(CategoryFactory)
    brand_name = random.choice(
        [
            "BMW",
            "Mercedes",
            "Volkswagen",
            "Opel",
            "Bugatti",
            "Lada",
            "Hyundai",
            "Toyota",
            "Kia",
        ]
    )
    seller = factory.SubFactory(SellerFactory)
    price = random.randrange(100000, 15000000, 10000)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            rnd = random.randint(1, 4)
            for i in range(min(rnd, len(extracted))):
                tag = extracted[random.randint(0, len(extracted) - 1)]
                self.tags.add(tag)


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=10)
    category = factory.SubFactory(CategoryFactory)
    seller = factory.SubFactory(SellerFactory)
    used = factory.Faker("pybool")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            rnd = random.randint(1, 4)
            for i in range(min(rnd, len(extracted))):
                tag = extracted[random.randint(0, len(extracted) - 1)]
                self.tags.add(tag)


class PictureFactory(DjangoModelFactory):
    class Meta:
        model = Picture

    img = "uploads/cars/" + download_image_from_url("https://picsum.photos/700/500")
    car = Car.objects.last()
