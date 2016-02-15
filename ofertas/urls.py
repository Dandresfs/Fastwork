from django.conf.urls import url
from .views import Ofertas

urlpatterns = [
    url(r'', Ofertas.as_view()),
]