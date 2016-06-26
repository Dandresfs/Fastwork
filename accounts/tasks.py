from __future__ import absolute_import, unicode_literals

from celery import shared_task
from mail_templated import send_mail
from Fastwork.settings.base import DEFAULT_FROM_EMAIL


@shared_task
def send_mail_template(template,parameters,to_email):
    send_mail(template, parameters, DEFAULT_FROM_EMAIL, to_email)
    pass