import logging

from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from main.models import Car, Item, Service, Subscriber
from django.core.mail import send_mail


from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)

interval = 3  # in minutes


def get_listings_by_created_range(model, time_from, time_to):
    """Get new listings."""
    result = "<div>"
    model_name = model._meta.model_name
    for obj in model.objects.filter(created_at__range=[time_from, time_to]):
        result += f'<a href="http://127.0.0.1:8000/{model_name}s/{obj.id}">{obj.title}</a> <br>'

    result += "</div>"
    return result


def notify_subscibers():
    """Send notifications."""
    current_time = (now(),)
    last_message_time = current_time[0] - timedelta(minutes=interval)
    new_car = get_listings_by_created_range(Car, last_message_time, current_time[0])
    new_item = get_listings_by_created_range(Item, last_message_time, current_time[0])
    new_service = get_listings_by_created_range(
        Service, last_message_time, current_time[0]
    )

    if new_car or new_item or new_service:
        subs = dict()
        for s in Subscriber.objects.all():
            if not subs.get(s.user.email):
                subs[s.user.email] = [s.subscribed_to]
            else:
                subs[s.user.email] += [s.subscribed_to]
        for email, subs_list in subs.items():
            message = "New listings: <br>"
            for sub_listing in subs_list:
                message += eval("new_" + sub_listing)
            send_mail(
                "New listings your interested in.",
                "",
                "no_reply@rynok.com",
                [email],
                html_message=message,
            )
