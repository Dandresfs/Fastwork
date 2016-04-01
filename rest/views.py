#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hv.models import Experiencia, Formacion
from .serializers import ExperienciaSerializer, FormacionSerializer
from rest_framework import mixins
from rest_framework import generics
import json
from django.http import HttpResponse
import Fastwork.settings.base as settings
from collections import OrderedDict

def departamentos(request):
    if request.method == 'GET':
        departamentos = json.load(open(settings.STATICFILES_DIRS[0]+"/json/municipios.json"))
        dict = {'':'----------'}
        try:
            departamento = departamentos[request.GET['departamento']]
        except KeyError:
            pass
        else:
            for municipio in departamento:
                dict[municipio] = municipio
        return HttpResponse(json.dumps(dict,sort_keys=True), content_type="application/json")

class ExperienciaApiView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):

    queryset = Experiencia.objects.all()
    serializer_class = ExperienciaSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExperienciaDetailApiView(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               generics.GenericAPIView):
    queryset = Experiencia.objects.all()
    serializer_class = ExperienciaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FormacionApiView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):

    queryset = Formacion.objects.all()
    serializer_class = FormacionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FormacionDetailApiView(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               generics.GenericAPIView):
    queryset = Formacion.objects.all()
    serializer_class = FormacionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)