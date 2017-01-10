from django.conf.urls import url
from .views import MisOfertasView, CrearEmpresaView, UpdateEmpresaView, ComprarCreditoEmpresa

urlpatterns = [
    url(r'^$', MisOfertasView.as_view()),
    url(r'^crearempresa/$', CrearEmpresaView.as_view()),
    url(r'^empresa/(?P<id_empresa>\w+)/$', UpdateEmpresaView.as_view()),
    url(r'^crearempresa/comprar/$', ComprarCreditoEmpresa.as_view()),
]