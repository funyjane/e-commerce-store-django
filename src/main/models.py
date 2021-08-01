from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


from .utils import random_string_generator


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=False)

    def unique_slug_generator(instance, new_slug=None):

        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(instance.title)

        Category = instance.__class__
        qs_exists = Category.objects.filter(slug=slug).exists()
        if qs_exists:
            new_slug = "{slug}-{randstr}".format(
                slug=slug, randstr=random_string_generator(size=4)
            )
            return unique_slug_generator(instance, new_slug=new_slug)
        return slug


def pre_save_category_receiver():
    pass


pre_save.connect(pre_save_category_receiver, sender=Category)


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def get_all_listings(self):

        listings = Listing.objects.filter(seller=self.user).count()

        if listings:
            return listings
        else:
            return "This seller has no listings"


class Tag(models.Model):
    title = models.CharField(max_length=100)


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    edited_at = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
