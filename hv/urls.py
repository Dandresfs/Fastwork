from django.conf.urls import url
from .views import Hv

urlpatterns = [
    url(r'', Hv.as_view()),
]