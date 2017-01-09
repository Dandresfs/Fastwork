from django.conf.urls import url
from .views import MisOfertasView, CrearEmpresaView

urlpatterns = [
    url(r'^$', MisOfertasView.as_view()),
    url(r'^crearempresa/$', CrearEmpresaView.as_view()),
]