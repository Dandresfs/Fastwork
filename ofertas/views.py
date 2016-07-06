from django.shortcuts import render
from django.views.generic import TemplateView
from ofertas.models import Categoria, Oferta
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SuperuserRequiredMixin
from ofertas.tables import AspirantesTable
from accounts.models import User
from ofertas.utils import PagedFilteredTableView
from ofertas.filters import AspiranteFilter
from ofertas.forms import AspiranteFilterFormHelper

class Ofertas(LoginRequiredMixin,TemplateView):
    template_name = 'ofertas/inicio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):

        categoria_render = []
        for categoria in Categoria.objects.all():
            cantidad = Oferta.objects.filter(categoria__id=categoria.id).count()
            if cantidad > 0:
                categoria_render.append({'nombre':categoria.nombre,'cantidad':cantidad,'id':categoria.id})

        departamento_render = []
        for departamento in Oferta.objects.all().values_list('departamento',flat=True).distinct():
            cantidad = Oferta.objects.filter(departamento=departamento).count()
            if cantidad > 0:
                departamento_render.append({'nombre':departamento,'cantidad':cantidad})

        ciudad_render = []
        for ciudad in Oferta.objects.all().values_list('municipio',flat=True).distinct():
            cantidad = Oferta.objects.filter(municipio=ciudad).count()
            if cantidad > 0:
                ciudad_render.append({'nombre':ciudad,'cantidad':cantidad})

        kwargs['total_ofertas'] = Oferta.objects.all().count()
        kwargs['categorias'] = categoria_render
        kwargs['total_departamentos'] = Oferta.objects.all().values_list('departamento',flat=True).count()
        kwargs['departamentos'] = departamento_render
        kwargs['total_ciudades'] = Oferta.objects.all().values_list('municipio',flat=True).count()
        kwargs['ciudades'] = ciudad_render
        return super(Ofertas,self).get_context_data(**kwargs)

class OfertaDetail(LoginRequiredMixin,TemplateView):
    template_name = 'ofertas/detail.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        oferta = Oferta.objects.get(id=self.kwargs['id_oferta'])
        kwargs['nombre_empresa'] = oferta.empresa.nombre_comercial
        kwargs['empresa_verificada'] = oferta.empresa.verificada
        kwargs['empresa_descripcion'] = oferta.empresa.descripcion

        try:
            kwargs['salario'] = '${:,.0f}'.format(int(oferta.salario))
        except:
            kwargs['salario'] = oferta.salario

        kwargs['oferta'] = oferta.titulo
        kwargs['descripcion'] = oferta.descripcion
        kwargs['fecha_contratacion'] = oferta.fecha_contratacion
        kwargs['vacantes'] = oferta.vacantes
        kwargs['educacion'] = oferta.educacion
        kwargs['experiencia'] = oferta.experiencia
        kwargs['disponibilidad_viajar'] = "Si" if oferta.viajar == True else "No"
        kwargs['disponibilidad_residencia'] = "Si" if oferta.residencia == True else "No"
        kwargs['aplicada'] = "Si" if oferta.aplicacion.filter(id=self.request.user.id).count() == 1 else "No"
        kwargs['cantidad_aplicadas'] = oferta.aplicacion.all().count()
        return super(OfertaDetail, self).get_context_data(**kwargs)

def aplicarOferta(request,id_oferta):
    if request.method == 'POST':
        oferta = Oferta.objects.get(id=id_oferta)
        oferta.aplicacion.add(request.user)
        oferta.save()
        return redirect('/ofertas/'+id_oferta+'/')
    else:
        return redirect('/ofertas/'+id_oferta+'/')

class OfertaComparativa(LoginRequiredMixin,TemplateView):
    template_name = 'ofertas/comparativa.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        oferta = Oferta.objects.get(id=self.kwargs['id_oferta'])
        kwargs['postulados'] = oferta.municipio
        kwargs['pk'] = self.kwargs['id_oferta']
        kwargs['total_aspirantes'] = oferta.aplicacion.all().count()
        return super(OfertaComparativa,self).get_context_data(**kwargs)

class OfertaEliminar(LoginRequiredMixin,TemplateView):
    template_name = 'ofertas/eliminar.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        oferta = Oferta.objects.get(id=self.kwargs['id_oferta'])
        kwargs['postulados'] = oferta.aplicacion.all()
        return super(OfertaEliminar,self).get_context_data(**kwargs)

class Seleccion(SuperuserRequiredMixin,TemplateView):
    template_name = 'ofertas/seleccionar.html'

    def get_context_data(self, **kwargs):
        return super(Seleccion, self).get_context_data(**kwargs)