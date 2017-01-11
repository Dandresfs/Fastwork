from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from empresa.models import Empresa, Checkouts
from empresa.forms import CrearEmpresaForm, UpdateEmpresaForm, ComprarCreditoEmpresaForm
import mercadopago
from Fastwork.settings.base import VALOR_EMPRESA
import os
import json
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
        kwargs['nombres'] = self.request.user.first_name
        kwargs['apellidos'] = self.request.user.last_name

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

    def percentage(self, percent, whole):
        return (percent * whole) / 100.0

    def form_valid(self, form):
        x = "8942863325364576"
        y = "cJJkiF3u6BTROwzMCiFgXQCjjzqTHw5L"
        mp = mercadopago.MP(x,y)

        valor_bruto = VALOR_EMPRESA * form.cleaned_data['cantidad']
        descuento = self.percentage(1 * int(form.cleaned_data['cantidad']),valor_bruto)

        preference = {
            "items": [
                {
                    "title": "Creditos para empresa",
                    "quantity": 1,
                    "currency_id": "COP",
                    "unit_price": valor_bruto-descuento,
                    "description": "Compra de " + str(form.cleaned_data['cantidad']) + " creditos para empresa."
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
            "back_urls": {
                "success":"http://fastworkcolombia.com/misofertas/mp/success/",
                "pending":"http://fastworkcolombia.com/misofertas/mp/pending/",
                "failure":"http://fastworkcolombia.com/misofertas/mp/failure/",
            }
        }

        preferenceResult = mp.create_preference(preference)
        url = preferenceResult["response"]["init_point"]
        response = preferenceResult["response"]

        nuevo = Checkouts()
        nuevo.user = self.request.user
        nuevo.id_mercadopago = response['id']
        nuevo.title = response['items'][0]['title']
        nuevo.description = response["items"][0]['description']
        nuevo.caterory_id = response["items"][0]['category_id']
        nuevo.quantity = response["items"][0]['quantity']
        nuevo.currency_id = response["items"][0]['currency_id']
        nuevo.unit_price = response["items"][0]["unit_price"]
        nuevo.name = response["payer"]["name"]
        nuevo.surname = response["payer"]["surname"]
        nuevo.email = response["payer"]["email"]
        nuevo.url_success = response["back_urls"]["success"]
        nuevo.url_pending = response["back_urls"]["pending"]
        nuevo.url_failure = response["back_urls"]["failure"]
        nuevo.init_point = response["init_point"]
        nuevo.sandbox_init_point = response["sandbox_init_point"]
        nuevo.save()

        return redirect(url)