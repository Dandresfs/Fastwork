from django.conf.urls import url
from .views import ExperienciaApiView, ExperienciaDetailApiView, FormacionApiView, FormacionDetailApiView,\
    departamentos, OfertasApiView,ComparativaApiView, SeleccionView, SeleccionRevisadoView,SeleccionSeleccionadoView,\
    MercadoPagoWebHookView

urlpatterns = [
    url(r'^departamentos/$', departamentos),
    url(r'^experiencia/$', ExperienciaApiView.as_view()),
    url(r'^experiencia/detail/(?P<pk>\d+)/$', ExperienciaDetailApiView.as_view()),
    url(r'^experiencia/update/(?P<pk>\d+)/$', ExperienciaDetailApiView.as_view()),
    url(r'^experiencia/delete/(?P<pk>\d+)/$', ExperienciaDetailApiView.as_view()),

    url(r'^formacion/$', FormacionApiView.as_view()),
    url(r'^formacion/detail/(?P<pk>\d+)/$', FormacionDetailApiView.as_view()),
    url(r'^formacion/update/(?P<pk>\d+)/$', FormacionDetailApiView.as_view()),
    url(r'^formacion/delete/(?P<pk>\d+)/$', FormacionDetailApiView.as_view()),

    url(r'^ofertas/$', OfertasApiView.as_view()),
    url(r'^ofertas/(?P<pk>\d+)/$', ComparativaApiView.as_view()),
    url(r'^seleccion/(?P<id_oferta>\d+)/$', SeleccionView.as_view()),
    url(r'^seleccion/revisado/$', SeleccionRevisadoView.as_view()),
    url(r'^seleccion/seleccionado/$', SeleccionSeleccionadoView.as_view()),

    url(r'^mercadopago/$', MercadoPagoWebHookView.as_view()),
]