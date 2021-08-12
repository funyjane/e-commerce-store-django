from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import ImageField

from .utils import unique_slug_generator


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Seller(User):
    code_inn = models.CharField(verbose_name="Tax Code", max_length=12, default="")
    img = ImageField(
        upload_to="uploads/profile_pics/",
        default="uploads/profile/default.png",
        null=False,
    )

    @property
    def get_all_listings(self):
        """
        return a number of all listing from the seller
        """

        listings = AbstractBaseListing.objects.filter(seller=self.user).count()

        if listings:
            return listings
        else:
            return "This seller has no listings"

    class Meta:
        verbose_name = "Seller"

    def __str__(self):
        return f"{self.username}"


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"


class AbstractBaseListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(blank=False, default=1)
    category = models.ForeignKey(
        Category, related_name="listing", null=True, on_delete=models.SET_NULL
    )
    seller = models.ForeignKey(
        Seller, null=True, related_name="listing", on_delete=models.SET_NULL
    )
    created_at = models.DateField(auto_now_add=True)
    edited_at = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="listing")

    def __str__(self):
        return f"{self.title}"


class Item(AbstractBaseListing):
    used = models.BooleanField(default=True)


class Car(AbstractBaseListing):
    brand_name = models.CharField(max_length=100)


class Service(AbstractBaseListing):
    type_of = models.CharField(max_length=100)


class ArchiveListing(AbstractBaseListing):
    class Meta:
        proxy = True
        ordering = ["created_at"]


class Picture(models.Model):

    img = ImageField(upload_to="uploads/cars/", null=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=False)
