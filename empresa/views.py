from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from empresa.models import Empresa
from empresa.forms import CrearEmpresaForm, UpdateEmpresaForm
# Create your views here.

class MisOfertasView(LoginRequiredMixin,TemplateView):
    template_name = 'empresas/inicio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        empresas = []
        ofertas = []

        for empresa in Empresa.objects.filter(propietario__id = self.request.user.id):
            empresas.append({'nombre':empresa.nombre_comercial,'logo':empresa.get_logo_url(),'nit':empresa.nit,
                             'descripcion':empresa.descripcion,'id':empresa.id})

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

    def dispatch(self, request, *args, **kwargs):
        cantidad_empresas = Empresa.objects.filter(propietario__id = self.request.user.id).count()
        if self.request.user.cantidad_empresas - cantidad_empresas > 0:
            return super(CrearEmpresaView,self).dispatch(request,*args,**kwargs)
        else:
            return redirect('/misofertas/crearempresa/comprar/')

class UpdateEmpresaView(LoginRequiredMixin,UpdateView):
    template_name = 'empresas/crearempresa.html'
    success_url = '/misofertas/'
    pk_url_kwarg = 'id_empresa'
    model = Empresa
    form_class = UpdateEmpresaForm

    def get_context_data(self, **kwargs):
        kwargs['nombre_comercial'] = self.object.nombre_comercial
        kwargs['razon_social'] = self.object.razon_social
        return super(UpdateEmpresaView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):

        empresas_id = Empresa.objects.filter(propietario__id = self.request.user.id).values_list('id',flat=True)

        if long(kwargs['id_empresa']) in empresas_id:
            return super(UpdateEmpresaView,self).dispatch(request,*args,**kwargs)
        else:
            return redirect('/misofertas/')