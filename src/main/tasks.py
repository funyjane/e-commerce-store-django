from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse

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
