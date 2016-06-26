#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from social.apps.django_app.default.models import UserSocialAuth
from mail_templated import send_mail
from Fastwork.settings.base import DEFAULT_FROM_EMAIL
import random
import string

from .forms import RegistrationForm, AccountForm
from .models import User, PreUser
from django.contrib.auth import login, authenticate
from accounts.tasks import send_mail_template


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(User.objects.make_random_password())
        obj.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/verification.html',
            'subject_template_name': 'registration/verification_subject.txt',
            'request': self.request,
            # 'html_email_template_name': provide an HTML content template if you desire.
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect('accounts:register-done')

class Perfil(UpdateView):
    model = User
    template_name = 'accounts/perfil.html'
    form_class = AccountForm
    success_url = '/ofertas/'

    def get_object(self):
        return User.objects.get(email=self.request.user.email)

    def get_context_data(self, **kwargs):
        kwargs['asociadas'] = UserSocialAuth.objects.filter(user=self.request.user).values_list('provider',flat=True)
        return super(Perfil,self).get_context_data(**kwargs)

def registration(request):
    if request.method == 'POST':
            email = request.POST['email']
            if User.objects.filter(email=email).count() == 0 and email != "" and PreUser.objects.filter(email=email).count() == 0:
                new = PreUser(email=email,password=request.POST['password'],username=request.POST['username'],first_name=request.POST['first_name'],
                              last_name=request.POST['last_name'],fullname=request.POST['first_name']+" "+request.POST['last_name'],
                              code="".join( [random.choice(string.letters) for i in xrange(15)] ))
                new.save()
                send_mail_template.delay('email/confirmation.tpl',{'email': new.email,'username':new.username,'fullname':new.fullname,'code':new.code,'password':request.POST['password']}, [new.email])
                #send_mail('email/confirmation.tpl', {'email': new.email,'username':new.username,'fullname':new.fullname,'code':new.code,'password':request.POST['password']}, DEFAULT_FROM_EMAIL, [new.email])
                return render(request, 'home.html', {'email':new.email})

            elif(PreUser.objects.filter(email=email).count() != 0):
                update = PreUser.objects.get(email=email)
                update.password = request.POST['password']
                update.code = "".join( [random.choice(string.letters) for i in xrange(15)] )
                update.save()
                send_mail_template.delay('email/confirmation.tpl', {'email': update.email,'username':update.username,'fullname':update.fullname,'code':update.code,'password':request.POST['password']}, [update.email])
                return render(request, 'home.html', {'email':update.email})

            elif User.objects.filter(email=email).count() != 0:
                return render(request, 'home.html', {'error_register':'El correo electrónico que ingreso ya esta registrado.'})

    return render(request, 'home.html', {})

def confirmation(request):
    if request.method == 'GET':
        email = request.GET['email']
        code = request.GET['code']
        if PreUser.objects.filter(email=email).count() != 0:
            preuser = PreUser.objects.get(email=email)
            if preuser.code == code:
                User.objects.create_user(email=preuser.email,password=preuser.password,username=preuser.username,
                                         first_name=preuser.first_name,last_name=preuser.last_name,fullname=preuser.fullname)
                preuser.delete()
                user = authenticate(email=email, password=preuser.password)
                login(request,user)
                return redirect('/')
            else:
                return redirect('/')

    return render(request, 'home.html', {})