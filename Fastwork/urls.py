from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from Fastwork.settings import base as settings
from django.contrib.auth import views as views_django_auth

urlpatterns = [
    url(r'^fastwork-admin/', admin.site.urls),
    # Python Social Auth URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    # Url de inicio
    url(r'^$', views_django_auth.login ,{'template_name':'home.html'}, name="home"),
    # Url de logout
    url(r'^logout/$', views_django_auth.logout, {'next_page': '/'}, name="user-logout"),

    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)