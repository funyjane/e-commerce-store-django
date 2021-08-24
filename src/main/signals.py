from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group

from .models import Subscriber, Item, Car, Service
from .tasks import email_subs_on_new_ad


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
            "",
            "admin@example.com",
            [instance.email],
            fail_silently=False,
            auth_user=None,
            auth_password=None,
            connection=None,
            html_message=render_to_string(
                "account/email/email_confirmation_message.html",
                context={"user": instance},
            ),
        )


@receiver(post_save, sender=Car)
@receiver(post_save, sender=Item)
@receiver(post_save, sender=Service)
def create_new_ad_actions(sender, instance, created, **kwargs):
    """
    sends email to Subscribers when new listing is created
    """
    if created:
        emails = [
            subs.user.email
            for subs in Subscriber.objects.filter(
                subscribed_to=instance._meta.model_name.capitalize()
            )
        ]
        email_subs_on_new_ad.delay(
            instance._meta.model_name,
            instance.pk,
            emails,
        )
