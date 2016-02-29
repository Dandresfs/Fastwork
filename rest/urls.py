from django.conf.urls import url
from .views import ExperienciaApiView, ExperienciaDetailApiView, FormacionApiView, FormacionDetailApiView

urlpatterns = [
    url(r'^experiencia/$', ExperienciaApiView.as_view()),
    url(r'^experiencia/detail/(?P<pk>\d+)/$', ExperienciaDetailApiView.as_view()),
    url(r'^experiencia/update/(?P<pk>\d+)/$', ExperienciaDetailApiView.as_view()),
    url(r'^experiencia/delete/(?P<pk>\d+)/$', ExperienciaDetailApiView.as_view()),

    url(r'^formacion/$', FormacionApiView.as_view()),
    url(r'^formacion/detail/(?P<pk>\d+)/$', FormacionDetailApiView.as_view()),
    url(r'^formacion/update/(?P<pk>\d+)/$', FormacionDetailApiView.as_view()),
    url(r'^formacion/delete/(?P<pk>\d+)/$', FormacionDetailApiView.as_view()),
]