#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hv.models import Experiencia, Formacion
from rest.serializers import ExperienciaSerializer, FormacionSerializer, OfertaSerializer
from rest_framework import mixins, pagination, response
from rest_framework import generics
import json
from django.http import HttpResponse
import Fastwork.settings.base as settings
from ofertas.models import Oferta
from django.db.models import Q
import operator

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



class OfertaPagination(pagination.PageNumberPagination):

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })



class OfertasApiView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):

    queryset = Oferta.objects.all().order_by('-publicacion')
    serializer_class = OfertaSerializer
    pagination_class = OfertaPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        palabra = self.request.query_params.get('palabra',None)
        categoria = self.request.query_params.get('categoria',None)
        departamento = self.request.query_params.get('departamento',None)
        municipio = self.request.query_params.get('municipio',None)

        filtros = []
        if palabra != '' and palabra != None:
            self.queryset = self.queryset.filter(Q(empresa__nombre_comercial__icontains=palabra)|
                                                 Q(categoria__nombre__icontains=palabra)|Q(titulo__icontains=palabra)|
                                                 Q(descripcion__icontains=palabra)|Q(departamento__icontains=palabra)|
                                                 Q(municipio__icontains=palabra))
        if categoria != 'todo' and categoria != None:
            filtros.append(Q(categoria__id=categoria))
        if departamento != 'todo' and departamento != None:
            filtros.append(Q(departamento=departamento))
        if municipio != 'todo' and municipio != None:
            filtros.append(Q(municipio=municipio))

        if len(filtros) > 0:
            return self.queryset.filter(reduce(operator.and_,filtros))
        else:
            return self.queryset.all()