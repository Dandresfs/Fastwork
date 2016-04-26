from django.shortcuts import render
from django.views.generic import TemplateView
from ofertas.models import Categoria, Oferta

class Ofertas(TemplateView):
    template_name = 'ofertas/inicio.html'

    def get_context_data(self, **kwargs):

        categoria_render = []
        for categoria in Categoria.objects.all():
            cantidad = Oferta.objects.filter(categoria__id=categoria.id).count()
            if cantidad > 0:
                categoria_render.append({'nombre':categoria.nombre,'cantidad':cantidad,'id':categoria.id})

        departamento_render = []
        for departamento in Oferta.objects.all().values_list('departamento',flat=True):
            cantidad = Oferta.objects.filter(departamento=departamento).count()
            if cantidad > 0:
                departamento_render.append({'nombre':departamento,'cantidad':cantidad})

        ciudad_render = []
        for ciudad in Oferta.objects.all().values_list('municipio',flat=True):
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