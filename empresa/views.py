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

# Create your views here.

class MisOfertasView(LoginRequiredMixin,TemplateView):
    template_name = 'empresas/inicio.html'
    login_url = '/'