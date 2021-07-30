from django.db import models


class Listing(models.Model):
    title = models.CharField(blank=False, null=False, max_length=100)
    description = models.TextField(blank=False, null=False)
    category = models.ForeignKey(Category, null=False, on_delete=models.SET_NULL)
    seller = models.ForeignKey(Owner, null=False, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    edited_at = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)


class Category(models.Model):
    pass


class Owner(models.Model):
    pass


class Tag(models.Model):
    pass
