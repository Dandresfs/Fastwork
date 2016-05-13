#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from datetime import datetime


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

    def get_queryset(self):
        queryset = Experiencia.objects.filter(user=self.request.user)
        return queryset

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

    def get_queryset(self):
        queryset = Formacion.objects.filter(user=self.request.user)
        return queryset

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


class ComparativaApiView(APIView):

    def get_object(self, pk):
        try:
            return Oferta.objects.get(pk=pk)
        except Oferta.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        oferta = self.get_object(pk)

        aplicados = oferta.aplicacion.all()
        aplicado_request = oferta.aplicacion.get(id=request.user.id)

        municipios = list(aplicados.values_list('ciudad',flat=True))
        municipios_si = municipios.count(oferta.municipio)
        municipios_no = len(municipios)-municipios_si

        r1 = 0
        r2 = 0
        r3 = 0
        r4 = 0
        r5 = 0
        r6 = 0
        r7 = 0

        for aplicado in aplicados:
            nacimiento = aplicado.fecha_nacimiento
            if nacimiento != None:
                edad = self.calcular_edad(nacimiento)
                if edad >= 18 and edad < 25:
                    r1 += 1
                if edad >= 25 and edad < 30:
                    r2 += 1
                if edad >= 30 and edad < 35:
                    r3 += 1
                if edad >= 35 and edad < 40:
                    r4 += 1
                if edad >= 40 and edad < 45:
                    r5 += 1
                if edad >= 45 and edad < 50:
                    r6 += 1
                if edad >= 50:
                    r7 += 1

        if aplicado_request.fecha_nacimiento != None:
            edad = self.calcular_edad(aplicado_request.fecha_nacimiento)

            if edad >= 18 and edad < 25:
                m = "18 y 24"
                r = r1
            if edad >= 25 and edad < 30:
                m = "25 y 29"
                r = r2
            if edad >= 30 and edad < 35:
                m = "30 y 34"
                r = r3
            if edad >= 35 and edad < 40:
                m = "35 y 39"
                r = r4
            if edad >= 40 and edad < 45:
                m = "40 y 44"
                r = r5
            if edad >= 45 and edad < 50:
                m = "45 y 49"
                r = r6
            if edad >= 50:
                m = "50 o mas"
                r = r7

            edad_porcentaje = self.percent(aplicados.exclude(fecha_nacimiento = None).count(),r)
            rango_edad = "El "+str(edad_porcentaje)+"% de los aspirantes tiene entre " + m + " años."
        else:
            rango_edad = "Debes actualizar esta informacion en tu perfil"







        return Response({'residencia':{'total':aplicados.count(),
                                       'si' : municipios_si,
                                       'no' : municipios_no,
                                       'si_porcentaje' : self.percent(aplicados.count(),municipios_si),
                                       'no_porcentaje' : self.percent(aplicados.count(),municipios_no),
                                       'ciudad' : oferta.municipio},
                         'edad':{'total':aplicados.count(),
                                 'edad':[r1,r2,r3,r4,r5,r6,r7],
                                 'rango':rango_edad}
                        })

    def percent(self,total,value):
        return round((value*100)/total)

    def calcular_edad(self,date):
        return int((datetime.date(datetime.now()) - date).days/365.2425)