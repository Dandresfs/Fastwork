from __future__ import unicode_literals

from django.db import models
from accounts.models import User

# Create your models here.
class Empresa(models.Model):
    propietario = models.ForeignKey(User,blank=True,null=True)
    nombre_comercial = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    nit = models.CharField(max_length=100,blank=True,null=True)
    departamento = models.CharField(max_length=100,blank=True,null=True)
    ciudad = models.CharField(max_length=100,blank=True,null=True)
    direccion = models.CharField(max_length=100,blank=True,null=True)
    sector = models.CharField(max_length=100,blank=True,null=True)
    cantidad_trabajadores = models.CharField(max_length=100,blank=True,null=True)

    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    pagina_web = models.URLField(max_length=100,blank=True)
    logo = models.ImageField(upload_to="Empresas/Logos",blank=True)

    contacto_nombres = models.CharField(max_length=100,blank=True,null=True)
    contacto_apellidos = models.CharField(max_length=100,blank=True,null=True)
    cargo = models.CharField(max_length=100,blank=True,null=True)
    telefono_1 = models.CharField(max_length=100,blank=True,null=True)
    telefono_2 = models.CharField(max_length=100,blank=True)

    verificada = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre_comercial

    def get_logo_url(self):
        try:
            url = self.logo.url
        except:
            url = ""
        return url

class Checkouts(models.Model):
    #Atributos sistema
    user = models.ForeignKey(User,blank=True,null=True)
    creation = models.DateTimeField(blank=True,null=True)
    tipo = models.CharField(max_length=100,blank=True,null=True)
    cantidad = models.IntegerField(blank=True,null=True)

    id_mercadopago = models.CharField(max_length=256,blank=True,null=True)
    title = models.CharField(max_length=256,blank=True,null=True)
    description = models.CharField(max_length=256,blank=True,null=True)
    caterory_id = models.CharField(max_length=256,blank=True,null=True)
    quantity = models.IntegerField(blank=True)
    currency_id = models.CharField(max_length=3,blank=True,null=True)
    unit_price = models.IntegerField(blank=True,null=True)

    name = models.CharField(max_length=256,blank=True,null=True)
    surname = models.CharField(max_length=256,blank=True,null=True)
    email = models.CharField(max_length=256,blank=True,null=True)

    url_success = models.URLField(max_length=600,blank=True,null=True)
    url_pending = models.URLField(max_length=600,blank=True,null=True)
    url_failure = models.URLField(max_length=600,blank=True,null=True)

    init_point = models.URLField(max_length=600,blank=True,null=True)
    sandbox_init_point = models.URLField(max_length=600,blank=True,null=True)

    status = models.CharField(max_length=256,blank=True,null=True)
    last_updated = models.DateTimeField(blank=True,null=True)