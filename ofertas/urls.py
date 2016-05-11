from django.conf.urls import url
from .views import Ofertas, OfertaDetail, aplicarOferta, OfertaComparativa

urlpatterns = [
    url(r'^$', Ofertas.as_view()),
    url(r'^(?P<id_oferta>\w+)/$', OfertaDetail.as_view()),
    url(r'^(?P<id_oferta>\w+)/aplicar/$', aplicarOferta),
    url(r'^(?P<id_oferta>\w+)/comparativa/$', OfertaComparativa.as_view()),
]