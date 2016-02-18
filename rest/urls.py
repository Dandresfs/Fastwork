from django.conf.urls import url
from .views import options

urlpatterns = [
    url(r'', options),
]