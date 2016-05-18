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


        rangos = [{"inferior":18,"superior":24,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":25,"superior":29,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":30,"superior":34,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":35,"superior":39,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":40,"superior":44,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":45,"superior":49,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":50,"superior":100,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":0,"superior":0,"cantidad":0,"porcentaje":0,"user_request":""},
                 ]

        for aplicado in aplicados:
            nacimiento = aplicado.fecha_nacimiento
            flag = False
            if aplicado == aplicado_request:
                flag = True

            if nacimiento != None:
                edad = self.calcular_edad(nacimiento)
                for rango in rangos:
                    if edad >= rango['inferior'] and edad < rango['superior'] and flag == False:
                        rango['cantidad'] += 1
                        rango['porcentaje'] = self.percent(aplicados.count(),rango['cantidad'])
                    if edad >= rango['inferior'] and edad < rango['superior'] and flag == True:
                        rango['cantidad'] += 1
                        rango['porcentaje'] = self.percent(aplicados.count(),rango['cantidad'])
                        rango['user_request'] = "El "+str(rango['porcentaje'])+"% de los aspirantes tiene entre "+str(rango['inferior'])+" y "+\
                                                str(rango['superior'])+" años."
            else:
                rango = rangos[7]
                rango['cantidad'] += 1
                rango['porcentaje'] = self.percent(aplicados.count(),rango['cantidad'])
                if flag == True:
                    rango['user_request'] = "Actualice su edad en la pestaña 'Mi perfil'"





        rangos_experiencia = [{"inferior":1,"superior":6,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":7,"superior":12,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":13,"superior":18,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":19,"superior":24,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":25,"superior":36,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":37,"superior":48,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":48,"superior":200,"cantidad":0,"porcentaje":0,"user_request":""},
                 {"inferior":0,"superior":0,"cantidad":0,"porcentaje":0,"user_request":""}
                 ]

        for aplicado in aplicados:
            experiencia = Experiencia.objects.filter(user=aplicado).count()

            flag = False
            if aplicado == aplicado_request:
                flag = True

            if experiencia > 0:
                experiencia = self.calcular_experiencia(aplicado)

                for rango in rangos_experiencia:
                    if experiencia >= rango['inferior'] and experiencia < rango['superior'] and flag == False:
                        rango['cantidad'] += 1
                        rango['porcentaje'] = self.percent(aplicados.count(),rango['cantidad'])
                    if experiencia >= rango['inferior'] and experiencia < rango['superior'] and flag == True:
                        rango['cantidad'] += 1
                        rango['porcentaje'] = self.percent(aplicados.count(),rango['cantidad'])
                        rango['user_request'] = "El "+str(rango['porcentaje'])+"% de los aspirantes tiene de "+str(rango['inferior'])+" a "+\
                                                str(rango['superior'])+" meses de experiencia."
            else:
                rango = rangos_experiencia[7]
                rango['cantidad'] += 1
                rango['porcentaje'] = self.percent(aplicados.count(),rango['cantidad'])
                if flag == True:
                    rango['user_request'] = "No tienes experiencia laboral registrada."






        return Response({'residencia':{'total':aplicados.count(),
                                       'si' : municipios_si,
                                       'no' : municipios_no,
                                       'si_porcentaje' : self.percent(aplicados.count(),municipios_si),
                                       'no_porcentaje' : self.percent(aplicados.count(),municipios_no),
                                       'ciudad' : oferta.municipio},
                         'edad':{'total':aplicados.count(),
                                 'edad':rangos,
                                },
                         'experiencia':{'total':aplicados.count(),
                                 'experiencia':rangos_experiencia,
                                }
                        })

    def percent(self,total,value):
        return round((value*100)/total)

    def calcular_edad(self,date):
        return int((datetime.date(datetime.now()) - date).days/365.2425)

    def calcular_experiencia(self,user):
        experiencias = Experiencia.objects.filter(user=user)
        meses = 0
        for experiencia in experiencias:
            meses += int(experiencia.meses)
        return meses