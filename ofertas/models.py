from __future__ import unicode_literals

from django.db import models
from empresa.models import Empresa
from accounts.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre

class Oferta(models.Model):
    empresa = models.ForeignKey(Empresa)
    categoria = models.ForeignKey(Categoria)
    titulo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)

    fecha_contratacion = models.DateField(editable=True,blank=True)
    cierre = models.DateField(blank=True,null=True)

    vacantes = models.IntegerField()
    salario = models.CharField(max_length=100)
    experiencia = models.BigIntegerField()

    viajar = models.BooleanField(default=False)
    educacion = models.CharField(max_length=100)
    residencia = models.BooleanField(default=False)

    descripcion = models.TextField(max_length=10000)

    publicacion = models.DateTimeField()
    publicacion.editable = True
    actualizacion = models.BooleanField(default=False)
    aplicacion = models.ManyToManyField(User,blank=True)


    def __unicode__(self):
        return self.empresa.nombre_comercial

class Revisado(models.Model):
    oferta = models.ForeignKey(Oferta)
    usuario = models.ForeignKey(User)

class Seleccionado(models.Model):
    oferta = models.ForeignKey(Oferta)
    usuario = models.ForeignKey(User)