from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from empresa.models import Empresa, Checkouts
from empresa.forms import CrearEmpresaForm, UpdateEmpresaForm, ComprarCreditoEmpresaForm
import mercadopago
import os
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

class ComprarCreditoEmpresa(LoginRequiredMixin,FormView):
    template_name = 'empresas/comprarcreditoempresa.html'
    success_url = '/misofertas/'
    form_class = ComprarCreditoEmpresaForm

    def get_initial(self):
        return {'user_id':self.request.user.id}

    def form_valid(self, form):
        x = "8942863325364576"
        y = "cJJkiF3u6BTROwzMCiFgXQCjjzqTHw5L"
        mp = mercadopago.MP(x,y)

        preference = {
            "items": [
                {
                    "title": "EMPRESA-" + str(self.request.user.id),
                    "quantity": form.cleaned_data['cantidad'],
                    "currency_id": "COP",
                    "unit_price": 100000
                }
            ],
            "payer": {
                "name": form.cleaned_data['nombres'],
                "surname": form.cleaned_data['apellidos'],
                "email": self.request.user.email,
                "phone": {
                    "area_code": "57",
                    "number": form.cleaned_data['telefono']
                },
                "identification": {
                    "type": "CC",
                    "number": form.cleaned_data['cedula']
                },
                "address": {
                    "street_name": form.cleaned_data['direccion'],
                }
            },
        }

        preferenceResult = mp.create_preference(preference)
        url = preferenceResult["response"]["init_point"]

        return redirect(url)