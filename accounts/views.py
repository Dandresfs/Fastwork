from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from social.apps.django_app.default.models import UserSocialAuth

from .forms import RegistrationForm, AccountForm
from .models import User

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