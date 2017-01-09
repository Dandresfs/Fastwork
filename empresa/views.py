from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from empresa.models import Empresa
# Create your views here.

class MisOfertasView(LoginRequiredMixin,TemplateView):
    template_name = 'empresas/inicio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        empresas = []

        for empresa in Empresa.objects.filter(propietario__id = self.request.user.id):
            empresas.append({'nombre':empresa.nombre_comercial,'logo':empresa.get_logo_url(),'nit':empresa.nit})

        kwargs['CANTIDAD_EMPRESAS'] = len(empresas)
        kwargs['EMPRESAS'] = empresas

        return super(MisOfertasView,self).get_context_data(**kwargs)