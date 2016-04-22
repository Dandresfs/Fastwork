from __future__ import unicode_literals

from django.db import models
from empresa.models import Empresa

# Create your models here.
class Oferta(models.Model):
    empresa = models.ForeignKey(Empresa)
    descripcion = models.TextField(max_length=10000)
    fecha_contratacion = models.DateField(blank=True)
    vacantes = models.IntegerField()
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    salario = models.CharField(max_length=100)
    educacion = models.CharField(max_length=100)
    experiencia = models.BigIntegerField()
    viajar = models.BooleanField(default=False)
    residencia = models.BooleanField(default=False)
    publicacion = models.DateTimeField(auto_now_add=True, blank=True)
    actualizacion = models.BooleanField(default=False)
    cierre = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.empresa