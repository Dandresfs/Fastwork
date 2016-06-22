import django_tables2 as tables
from accounts.models import User
from django.utils.safestring import mark_safe

class AspirantesTable(tables.Table):
    fullname = tables.Column(verbose_name="Nombre")
    departamento = tables.Column(verbose_name="Departamento")
    ciudad = tables.Column(verbose_name="Ciudad")
    email = tables.Column(verbose_name="Email")
    telefono_1 = tables.Column(verbose_name="Telefono")
    experiencia = tables.Column(verbose_name="Experiencia",accessor='get_experiencia_cantidad')
    hv = tables.Column(verbose_name="Hv")

    def render_hv(self,value):
        return mark_safe('<a href="'+value.url+'" target="_blank"><img height="42" width="42" src="/static/imagenes/file.png"></p>')

    class Meta:
        model = User
        fields = ('fullname','departamento','ciudad','email','telefono_1','experiencia','hv')
        attrs = {"class": "table table-bordered"}