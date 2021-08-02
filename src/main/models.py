from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


from .utils import unique_slug_generator


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Category, self).save(*args, **kwargs)


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
