from django.shortcuts import render
from django.views.generic import UpdateView
from social.apps.django_app.default.models import UserSocialAuth
from .forms import ProfesionalForm
from accounts.models import User

# Create your views here.
class Hv(UpdateView):
    model = User
    template_name = 'hv/inicio.html'
    form_class = ProfesionalForm
    success_url = '/ofertas/'

    def get_object(self):
        return User.objects.get(email=self.request.user.email)

    def get_context_data(self, **kwargs):
        kwargs['asociadas'] = UserSocialAuth.objects.filter(user=self.request.user).values_list('provider',flat=True)
        return super(Hv,self).get_context_data(**kwargs)