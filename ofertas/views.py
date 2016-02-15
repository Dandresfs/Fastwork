from django.shortcuts import render
from django.views.generic import TemplateView

class Ofertas(TemplateView):
    template_name = 'ofertas/inicio.html'