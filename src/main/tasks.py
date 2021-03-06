import uuid
import json

from django.utils.timezone import now
from django.core.mail import send_mail
from django.urls import reverse
from datetime import timedelta
from celery.utils.log import get_task_logger
from celery import shared_task
from twilio.rest import Client


from main.administration.tasks.tasks import get_listings_by_created_range
from main import models


logger = get_task_logger(__name__)


@shared_task
def email_subs_on_new_ad(model_name, pk, emails):
    logger.info("Sent new listing email")
    send_mail(
        "New listing at example.com",
        "",
        "admin@example.com",
        emails,
        html_message=f'You have subscribed to new {model_name}s listings. New listings have been placed just now. \
              <a href="http://example.com'
        + f"{reverse('main:'+model_name+'-details', args=(pk,))}\">See details</a>",
    )


@shared_task
def new_lisings_week():
    """Send weekly notifications."""
    current_time = now()
    last_message_time = current_time - timedelta(days=7)
    new_car = get_listings_by_created_range(models.Car, last_message_time, current_time)
    new_item = get_listings_by_created_range(
        models.Item, last_message_time, current_time
    )
    new_service = get_listings_by_created_range(
        models.Service, last_message_time, current_time
    )

    if new_car or new_item or new_service:
        subs = dict()
        for sub in models.Subscriber.objects.all():
            if not subs.get(sub.user.email):
                subs[sub.user.email] = [sub.subscribed_to]
            else:
                subs[sub.user.email] += [sub.subscribed_to]
        for email, subs_list in subs.items():
            message = "New listings: <br>"
            for sub_listing in subs_list:
                message += eval("new_" + sub_listing)
            send_mail(
                "New weekly listings you interested in.",
                "",
                "no_reply@rynok.com",
                [email],
                html_message=message,
            )


@shared_task
def verify_phone(phone, sid, token, from_phone, user_id):
    secret = uuid.uuid4().hex[:4]
    phone_number = phone
    phone_from = from_phone
    account_sid = sid
    auth_token = token
    client = Client(account_sid, auth_token)
    response = client.messages.create(
        body=f"Your code {secret}", from_=phone_from, to=phone_number
    )
    seller = models.Seller.objects.get(id=user_id)
    models.SMSLog.objects.create(
        secret_code=secret, seller=seller, response_twillio=response.sid
    )
