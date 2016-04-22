from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Empresa(models.Model):
    nombre_comercial = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    nit = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    cantidad_trabajadores = models.CharField(max_length=100)

    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    pagina_web = models.URLField(max_length=100,blank=True)
    logo = models.ImageField(upload_to="Empresas/Logos",blank=True)

    contacto_nombres = models.CharField(max_length=100)
    contacto_apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono_1 = models.CharField(max_length=100)
    telefono_2 = models.CharField(max_length=100,blank=True)

    verificada = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre_comercial