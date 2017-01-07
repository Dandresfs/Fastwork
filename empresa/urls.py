from django.conf.urls import url
from .views import MisOfertasView

urlpatterns = [
    url(r'^$', MisOfertasView.as_view()),
]