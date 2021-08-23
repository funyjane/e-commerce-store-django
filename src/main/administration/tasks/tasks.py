import logging

from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from main.models import Car, Item, Service, Subscriber
from django.core.mail import send_mail


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)

interval = 3  # in minutes


def mail_about_new_ads():
    # Your job processing logic here...
    now_time = now()
    logger.info("Starting mail_about_new_ads scheduled job at:", now_time.time())
    prev_time = now_time - timedelta(minutes=interval)
    cars = "<br>\n".join(
        [
            f'<a href="http://localhost:8000/cars/{str(car.id)}">{car.title}</a>'
            for car in Car.objects.filter(created_at__range=[prev_time, now_time])
        ]
    )
    items = "<br>\n".join(
        [
            f'<a href="http://localhost:8000/items/{str(item.id)}">{item.title}</a>'
            for item in Item.objects.filter(created_at__range=[prev_time, now_time])
        ]
    )
    services = "<br>\n".join(
        [
            f'<a href="http://localhost:8000/services/{str(service.id)}">{service.title}</a>'
            for service in Service.objects.filter(
                created_at__range=[prev_time, now_time]
            )
        ]
    )

    if cars or items or services:
        subscribers = dict()
        all_subs = Subscriber.objects.all()
        for sub in all_subs:
            if all_subs.exists():
                subscribers[sub.user.email] = [sub.subscribed_to]
                send_mail(
                    "New listings at example.com",
                    "",
                    "admin@example.com",
                    sub.user.email,
                    html_message="You have subscribed to new listings. New listings have been placed just now:<br>\n"
                    + eval("+".join(sub.subscribed_to)),
                )


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            mail_about_new_ads,
            trigger=CronTrigger(minute="*/" + str(interval)),  # Every 10 seconds
            id="mail_about_new_ads",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'mail_about_new_ads'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
