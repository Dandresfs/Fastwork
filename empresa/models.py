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

    tipo = models.CharField(max_length=100,blank=True,null=True)
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