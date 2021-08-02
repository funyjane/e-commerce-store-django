from django.test import TestCase
from django.contrib.auth.models import User

from .models import Seller, AbstractBaseListing, Category, Tag

# Create your tests here.


class ModelTests(TestCase):
    def set_up(self):
        self.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@email.com",
            password="testpass1",
        )

        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@email.com",
            password="testpass2",
        )

        self.seller = Seller.objects.create(user=self.user)

        self.seller2 = Seller.objects.create(user=self.user2)

        self.category = Category.objects.create(name="TestCategory1")

        self.category2 = Category.objects.create(name="TestCategory2")

        self.tag = Tag.objects.create(name="TestTag1")

        self.tag2 = Tag.objects.create(name="TestTag2")

        self.listing = AbstractBaseListing.objects.create(
            name="TestListing1",
            description="This is TestListing1 object description",
            category=self.category,
            seller=self.seller,
        )

        self.ad.tags.add(self.tag)

        self.listing2 = AbstractBaseListing.objects.create(
            name="TestListing2",
            description="This is TestListing2 object description",
            category=self.category2,
            seller=self.seller2,
        )

        self.ad2.tags.add(self.tag2)

    def test_users(self):
        self.assertIn(self.user, User.objects.all(), "no user!")
        self.assertIn(self.user2, User.objects.all(), "no user2!")
        self.user2.username = "testuser2_test_edit"
        self.assertNotEqual(
            User.objects.get(email="testuser2@email.com").username,
            "testuser2_test_edit",
        )
        self.user2.save()
        self.assertEqual(
            User.objects.get(email="testuser2@email.com").username,
            "testuser2_test_edit",
        )

    def test_sellers(self):
        self.assertIn(self.seller, Seller.objects.all(), "no seller")
        self.assertIn(
            self.seller2,
            Seller.objects.filter(user__username__startswith="test"),
            "cant find seller2",
        )
        self.assertEqual(self.seller.user, self.user, "seller and user not equal")

    def test_categories(self):
        self.assertEqual(
            2,
            Category.objects.filter(name__startswith="TestCategory").count(),
            "categories count not equal",
        )

    def test_tags(self):
        t = Tag(name="TestTag3")
        t.save()
        self.assertEqual(self.tag.ad_set.all()[0], self.ad, "tag problem")
        qs = AbstractBaseListing.objects.all()
        for listing in qs:
            listing.tags.add(t)
        self.assertEqual(list(qs), list(t.ad_set.all()), "tags are not equal")

    def test_listings(self):
        self.test_tags()
        ad = AbstractBaseListing.objects.get(seller__user__username="testuser1")
        self.assertEqual(ad.category, self.category)
        qs = ad.tags.all().values_list("name", flat=True)
        self.assertIn("TestTag1", qs)
        self.assertIn("TestTag3", qs)
        self.assertEqual(ad.category.name, "TestCategory1")
        new_ad = AbstractBaseListing.objects.create(
            name="TestListing3",
            description="This is TestListing1 object description",
            category=self.category,
            seller=self.seller,
        )

        new_ad.tags.add(self.tag)

        new_ad2 = AbstractBaseListing(
            name="TestListing4",
            description="This is TestListing1 object description",
            category=self.category2,
            seller=self.seller2,
        )
        new_ad2.save()
        new_ad2.tags.add(self.tag2)
        self.assertEqual(
            ["TestListing1", "TestListing3"],
            list(
                AbstractBaseListing.objects.filter(category=self.category).values_list(
                    "name", flat=True
                )
            ),
        )
        self.assertEqual(
            ["TestListing2", "TestListing4"],
            list(
                AbstractBaseListing.objects.filter(category=self.category2).values_list(
                    "name", flat=True
                )
            ),
        )
