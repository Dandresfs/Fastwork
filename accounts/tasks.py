from __future__ import absolute_import, unicode_literals

from celery import shared_task
from mail_templated import send_mail
from Fastwork.settings.base import DEFAULT_FROM_EMAIL
from accounts.models import PreUser


@shared_task
def send_mail_template(template,parameters,to_email):
    pre_user = PreUser.objects.get(email=parameters['email'])
    try:
        send_mail(template, parameters, DEFAULT_FROM_EMAIL, to_email)
    except:
        pre_user.mail_send = False
    else:
        pre_user.mail_send = True
    pre_user.save()
    return "Ok"


@shared_task
def re_send_mail():
    pre_users = PreUser.objects.filter(mail_send=False).order_by('-id')
    if pre_users.count() != 0:
        pre_user = pre_users[0]
        try:
            send_mail('email/confirmation.tpl', {'email': pre_user.email,'username':pre_user.username,'fullname':pre_user.fullname,'code':pre_user.code,'password':pre_user.password}, DEFAULT_FROM_EMAIL ,[pre_user.email])
        except:
            pre_user.mail_send = False
            mensaje = "error"
        else:
            pre_user.mail_send = True
            mensaje = "enviado"
        pre_user.save()
    else:
        mensaje = "no hay pre usuarios"
    return mensaje