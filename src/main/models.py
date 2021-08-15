from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db import models
from sorl.thumbnail import ImageField

from .utils import validate_inn
from .utils import unique_slug_generator


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Assign the default common_users group to every new user
    """
    if created:
        instance.groups.add(Group.objects.get_or_create(name="common users")[0].id)
        """
        Send welcome msg
        """
        send_mail(
            "Welcome at rynok.com",
            f"Welcome {instance.username} please stay with us!",
            "admin@example.com",
            [instance.email],
            fail_silently=False,
            auth_user=None,
            auth_password=None,
            connection=None,
            html_message=None,
        )


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
    code_inn = models.CharField(
        verbose_name="Tax Code", max_length=12, default="", validators=[validate_inn]
    )
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

    def __str__(self):
        return f"{self.img.path}"
