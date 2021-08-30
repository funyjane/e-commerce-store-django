from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Item, Seller, AbstractBaseListing, Category, Tag, Car, Item, Service

# Create your tests here.

User = get_user_model()


class ModelTests(TestCase):
    def set_up(self):
        self.user = User.objects.create_user(
            username="testuser136",
            email="testuser1@email.com",
            password="testpass136",
        )
        self.user2 = User.objects.create_user(
            username="testuser257",
            email="testuser2@email.com",
            password="testpass257",
        )

        self.client.force_login(self.user)

        self.seller = Seller.objects.create(username="NewSellerUsername1")
        self.seller2 = Seller.objects.create(username="NewSellerUsername2")

        self.category = Category.objects.create(title="TestCategory1")
        self.category2 = Category.objects.create(title="TestCategory2")

        self.tag = Tag.objects.create(title="TestTag1")
        self.tag2 = Tag.objects.create(title="TestTag2")

        self.car_ad = Car.objects.create(
            title="TestAd1",
            description="This is test1 Ad object description",
            category=self.category,
            seller=self.seller,
            brand_name="BMW",
        )
        self.car_ad.tags.add(self.tag)

        self.car_ad2 = Car.objects.create(
            title="TestAd2",
            description="This is test2 Ad object description",
            category=self.category,
            seller=self.seller,
            brand_name="Carrerino",
        )
        self.car_ad2.tags.add(self.tag2)

        self.item_ad = Item.objects.create(
            title="TestThingAd1",
            description="Test",
            category=self.category,
            seller=self.seller,
            used=True,
        )

        self.service_ad = Service.objects.create(
            title="TestThingAd12",
            description="Test",
            category=self.category,
            seller=self.seller,
            type_of="near",
        )

    def test_views_response_status_codes(self):

        """Test views response status codes"""

        views_names = [
            "main:car-catalog",
            "main:item-catalog",
            "main:service-catalog",
            "main:listing-catalog",
            "main:car-create",
            "main:item-create",
            "main:service-create",
        ]
        for view in views_names:
            response = self.client.get(reverse(view))
            self.assertEquals(
                response.status_code,
                200,
                f"status code: {response.status_code}, has to be 200",
            )

        self.assertEqual(
            self.client.get(
                reverse("main:car-details", kwargs={"pk": self.car_ad.pk})
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:item-details", kwargs={"pk": self.item_ad.pk})
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:service-details", kwargs={"pk": self.service_ad.pk})
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:car-update", kwargs={"pk": self.car_ad.pk})
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:item-update", kwargs={"pk": self.item_ad.pk})
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:service-update", kwargs={"pk": self.service_ad.pk})
            ).status_code,
            200,
        )
