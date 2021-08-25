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


# def mail_about_new_ads():
#     # Your job processing logic here...
#     now_time = now()
#     logger.info("Starting mail_about_new_ads scheduled job at:", now_time.time())
#     prev_time = now_time - timedelta(minutes=interval)
#     cars = "<br>\n".join(
#         [
#             f'<a href="http://localhost:8000/cars/{str(car.id)}">{car.title}</a>'
#             for car in Car.objects.filter(created_at__range=[prev_time, now_time])
#         ]
#     )
#     items = "<br>\n".join(
#         [
#             f'<a href="http://localhost:8000/items/{str(item.id)}">{item.title}</a>'
#             for item in Item.objects.filter(created_at__range=[prev_time, now_time])
#         ]
#     )
#     services = "<br>\n".join(
#         [
#             f'<a href="http://localhost:8000/services/{str(service.id)}">{service.title}</a>'
#             for service in Service.objects.filter(
#                 created_at__range=[prev_time, now_time]
#             )
#         ]
#     )

#     if cars or items or services:
#         subscribers = dict()
#         all_subs = Subscriber.objects.all()
#         for sub in all_subs:
#             if all_subs.exists():
#                 subscribers[sub.user.email] = [sub.subscribed_to]
#                 send_mail(
#                     "New listings at example.com",
#                     "",
#                     "admin@example.com",
#                     sub.user.email,
#                     html_message="You have subscribed to new listings. New listings have been placed just now:<br>\n"
#                     + eval("+".join(sub.subscribed_to)),
#                 )
