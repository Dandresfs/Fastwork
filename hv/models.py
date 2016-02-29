from __future__ import unicode_literals

from django.db import models
import datetime
from accounts.models import User

class Experiencia(models.Model):
    user = models.ForeignKey(User)
    empresa = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    periodo = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    funciones_logros = models.TextField(max_length=500,blank=True)
    meses = models.IntegerField(blank=True)


class Formacion(models.Model):
    user = models.ForeignKey(User)
    institucion = models.CharField(max_length=100)
    nivel = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    periodo = models.CharField(max_length=50)