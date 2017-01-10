from django.conf.urls import url
from .views import MisOfertasView, CrearEmpresaView, UpdateEmpresaView

urlpatterns = [
    url(r'^$', MisOfertasView.as_view()),
    url(r'^crearempresa/$', CrearEmpresaView.as_view()),
    url(r'^empresa/(?P<id_empresa>\w+)/$', UpdateEmpresaView.as_view()),
]