from django.contrib import admin
from ofertas.models import Oferta, Categoria

# Register your models here.
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['empresa','titulo','descripcion']
admin.site.register(Oferta,OfertaAdmin)
admin.site.register(Categoria)