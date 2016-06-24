from __future__ import absolute_import

from celery import shared_task
from mail_templated import send_mail
from Fastwork.settings.base import DEFAULT_FROM_EMAIL


@shared_task
def send_mail_template(template,parameters,from_email,to_email):
    send_mail(template, parameters, from_email, to_email)
    pass