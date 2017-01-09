from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from empresa.models import Empresa
from empresa.forms import CrearEmpresaForm
# Create your views here.

class MisOfertasView(LoginRequiredMixin,TemplateView):
    template_name = 'empresas/inicio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        empresas = []
        ofertas = []

        for empresa in Empresa.objects.filter(propietario__id = self.request.user.id):
            empresas.append({'nombre':empresa.nombre_comercial,'logo':empresa.get_logo_url(),'nit':empresa.nit,
                             'descripcion':empresa.descripcion})

        kwargs['CANTIDAD_EMPRESAS'] = len(empresas)
        kwargs['CANTIDAD_EMPRESAS_DISPONIBLE'] = self.request.user.cantidad_empresas - len(empresas)
        kwargs['CANTIDAD_OFERTAS'] = len(ofertas)
        kwargs['CANTIDAD_OFERTAS_DISPONIBLE'] = self.request.user.cantidad_ofertas - len(ofertas)
        kwargs['EMPRESAS'] = empresas
        kwargs['OFERTAS'] = ofertas

        return super(MisOfertasView,self).get_context_data(**kwargs)

class CrearEmpresaView(LoginRequiredMixin,CreateView):
    template_name = 'empresas/crearempresa.html'
    success_url = '/misofertas/'
    model = Empresa
    form_class = CrearEmpresaForm

    def get_initial(self):
        return {'user_id':self.request.user.id}