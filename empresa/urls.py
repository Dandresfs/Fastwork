from django.conf.urls import url
from .views import MisOfertasView, CrearEmpresaView, UpdateEmpresaView, ComprarCreditoEmpresa, ComprarCreditoOferta, CrearOfertaView

urlpatterns = [
    url(r'^$', MisOfertasView.as_view()),
    url(r'^crearempresa/$', CrearEmpresaView.as_view()),
    url(r'^crearoferta/$', CrearOfertaView.as_view()),
    url(r'^empresa/(?P<id_empresa>\w+)/$', UpdateEmpresaView.as_view()),
    url(r'^crearempresa/comprar/$', ComprarCreditoEmpresa.as_view()),
    url(r'^crearoferta/comprar/$', ComprarCreditoOferta.as_view()),
]