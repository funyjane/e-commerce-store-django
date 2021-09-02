from logging import PlaceHolder
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from sorl.thumbnail import ImageField
from phonenumber_field.modelfields import PhoneNumberField

from main.utils import validate_inn, unique_slug_generator

from main.tasks import verify_phone


class Subscriber(models.Model):
    """
    Subscriber used as a mailing list for subscribed Users
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_to = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user}, subscribed to: {self.subscribed_to}"


class Category(models.Model):
    """
    Category model instance
    """

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """
        Generates a unique slug field based on the tite
        """
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Seller(User):
    """
    Category model instance
    """

    code_inn = models.CharField(
        verbose_name="Tax Code",
        max_length=12,
        default="000000000000",
        validators=[validate_inn],
    )
    img = ImageField(
        upload_to="uploads/profile_pics/",
        default="uploads/profile/default.png",
        null=False,
    )
    phone_number = PhoneNumberField(
        null=True,
        verbose_name="Phone",
        error_messages={"invalid": "Phone number must be valid"},
        unique=True,
        blank=True,
        default="",
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

    def save(self, *args, **kwargs):
        """
        sends out a verification msg to when new Seller instance is created
        """

        super().save(*args, **kwargs)

        verify_phone.delay(
            self.phone_number.as_e164,
            settings.ACCOUNT_SID,
            settings.AUTH_TOKEN,
            settings.PHONE_FROM,
            self.user_ptr_id,
        )

    class Meta:
        verbose_name = "Seller"

    def __str__(self):
        return f"{self.username}"


class Tag(models.Model):
    """
    Tag model instance
    """

    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"


class AbstractBaseListing(models.Model):
    """
    Main Listing model instance - serves as abstract model class
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(blank=False, default=1)
    category = models.ForeignKey(
        Category, related_name="listing", null=True, on_delete=models.SET_NULL
    )
    seller = models.ForeignKey(
        Seller, null=True, related_name="listing", on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="listing")
    phone_number = PhoneNumberField(
        null=True,
        verbose_name="Phone",
        error_messages={"invalid": "Phone number must be valid"},
        unique=True,
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.title}"


class Item(AbstractBaseListing):
    """
    Item model instance
    """

    used = models.BooleanField(default=True)


class Car(AbstractBaseListing):
    """
    Item model instance
    """

    brand_name = models.CharField(max_length=100)


class Service(AbstractBaseListing):
    """
    Item model instance
    """

    type_of = models.CharField(max_length=100)


class ArchiveListing(AbstractBaseListing):
    """
    ArchiveListing model instance - used to register AbstractListing in admin.py
    """

    class Meta:
        proxy = True
        ordering = ["created_at"]


class Picture(models.Model):
    """
    picture field for Car model instance
    """

    img = ImageField(upload_to="uploads/cars/", null=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.img.path}"


class SMSLog(models.Model):
    """
    Twillio logs model
    """

    seller = models.ForeignKey(
        "Seller",
        verbose_name="Seller",
        related_name="smslogs",
        on_delete=models.CASCADE,
    )

    secret_code = models.CharField(
        verbose_name="Phone confirmation code",
        max_length=4,
        blank=True,
        null=True,
        default="",
    )

    response_twillio = models.TextField(
        verbose_name="Provider's response",
        blank=True,
        null=True,
        default="",
    )

    def __str__(self):
        return str(self.secret_code)

    class Meta:
        verbose_name = "SMS Journal"
        verbose_name_plural = "SMS Journals"
