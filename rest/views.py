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
from braces.views import LoginRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from accounts.models import User
from ofertas.models import Seleccionado, Revisado
from django.db.models import Q
import mercadopago
from empresa.models import Checkouts



class MercadoPagoWebHookView(APIView):

    def get(self, request, format=None):
        return HttpResponse(status = 300)

    def post(self, request, format=None):
        """
        try:
            id = request.query_params.get('id')
        except:
            id = None
        try:
            topic = request.query_params.get('topic')
        except:
            topic = None

        if id != None and topic != None:
            mp = mercadopago.MP("8942863325364576", "cJJkiF3u6BTROwzMCiFgXQCjjzqTHw5L")


            merchant_order_info = None

            if topic == "payment":
                payment_info = mp.get("/collections/notifications/" + id)
                merchant_order_info = mp.get("/merchant_orders/"+payment_info["response"]["collection"]["merchant_order_id"])

            elif topic == "merchant_order":
                merchant_order_info = mp.get("/merchant_orders/" + id)

            if merchant_order_info == None:
                raise ValueError("Error obtaining the merchant_order")

            if merchant_order_info["status"] == 200:
                c = {
                    "payment": merchant_order_info["response"]["payments"],
                    "shipment": merchant_order_info["response"]["shipments"]
                }
                Checkouts.objects.all()[0].update(description = unicode(c))
        """
        Checkouts.objects.all()[0].update(description = request.query_params)
        return HttpResponse(status = 200)

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

class ExperienciaApiView(LoginRequiredMixin,
                         mixins.ListModelMixin,
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


class ExperienciaDetailApiView(LoginRequiredMixin,
                               mixins.RetrieveModelMixin,
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


class FormacionApiView(LoginRequiredMixin,
                       mixins.ListModelMixin,
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


class FormacionDetailApiView(LoginRequiredMixin,
                             mixins.RetrieveModelMixin,
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



        residencia = [{"municipio":"si","cantidad":0,"porcentaje":0,"user_request":""},
                      {"municipio":"otro","cantidad":0,"porcentaje":0,"user_request":""},
                      {"municipio":"ninguno","cantidad":0,"porcentaje":0,"user_request":""},
                     ]



        for aplicado in aplicados:
            r = aplicado.ciudad
            flag = False
            if aplicado == aplicado_request:
                flag = True

            if r == "":
                residencia[2]['cantidad'] += 1
                residencia[2]['porcentaje'] = self.percent(aplicados.count(),residencia[2]['cantidad'])
                if flag == True:
                    residencia[2]['user_request'] = "Actualiza tus datos de residencia"

            elif r == oferta.municipio:
                residencia[0]['cantidad'] += 1
                residencia[0]['porcentaje'] = self.percent(aplicados.count(),residencia[0]['cantidad'])
                if flag == True:
                    residencia[2]['user_request'] = "El "+str(residencia[0]['porcentaje'])+"% de los aspirantes reside en "+oferta.municipio+"."
            else:
                residencia[1]['cantidad'] += 1
                residencia[1]['porcentaje'] = self.percent(aplicados.count(),residencia[1]['cantidad'])
                if flag == True:
                    residencia[2]['user_request'] = "El "+str(residencia[2]['porcentaje'])+"% de los aspirantes no reside en "+oferta.municipio+"."



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
                    rango['user_request'] = "Actualiza tu edad en la pestaña 'Mi perfil'"





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






        niveles = [{"nivel":"Básico","cantidad":0,"porcentaje":0,"user_request":""},
                      {"nivel":"Medio","cantidad":0,"porcentaje":0,"user_request":""},
                      {"nivel":"Universitario","cantidad":0,"porcentaje":0,"user_request":""},
                      {"nivel":"de Postgrado","cantidad":0,"porcentaje":0,"user_request":""},
                      {"nivel":"Nada","cantidad":0,"porcentaje":0,"user_request":""},
                     ]



        for aplicado in aplicados:
            flag = False
            if aplicado == aplicado_request:
                flag = True

            n = self.establecer_nivel(aplicado)

            for nivel in niveles:
                if nivel['nivel'] == n:
                    nivel['cantidad'] += 1
                    nivel['porcentaje'] = self.percent(aplicados.count(),nivel['cantidad'])
                    if flag == True and nivel['nivel'] == "Nada":
                        nivel['user_request'] = "Actualiza tus datos de formación"
                    if flag == True and nivel['nivel'] != "Nada":
                        nivel['user_request'] = "El "+unicode(nivel['porcentaje'])+"% de los aspirates tiene formación a nivel "+nivel['nivel']+"."






        return Response({'residencia':{'total':aplicados.count(),
                                 'residencia':residencia,
                                },
                         'edad':{'total':aplicados.count(),
                                 'edad':rangos,
                                },
                         'experiencia':{'total':aplicados.count(),
                                 'experiencia':rangos_experiencia,
                                },
                         'nivel':{'total':aplicados.count(),
                                 'nivel':niveles,
                                },
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

    def establecer_nivel(self,user):
        formaciones = Formacion.objects.filter(user=user).values_list('nivel',flat=True)
        if formaciones.count() == 0:
            return "Nada"
        for formacion in formaciones:
            if formacion == "Educación Básica Primaria" or formacion == "Educación Básica Secundaria":
                return "Básico"
            elif formacion == "Bachillerato / Educación Media":
                return "Medio"
            elif formacion == "Universidad / Carrera técnica" or formacion == "Universidad / Carrera tecnológica" or formacion == "Universidad / Carrera Profesional":
                return "Universitario"
            elif formacion == "Postgrado / Especialización" or formacion == "Postgrado / Maestría" or formacion == "Postgrado / Doctorado":
                return "de Postgrado"
            else:
                return "Nada"


class SeleccionRevisadoView(LoginRequiredMixin,
                             mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               generics.GenericAPIView):

    def put(self, request, *args, **kwargs):
        ofertas_ids = [8,28,9,33,10,37,11,40,61,63,64]
        ofertas_ids2 = [45,52,65]
        if int(request.POST['oferta']) in ofertas_ids:
            for oferta_id in ofertas_ids:
                o = Oferta.objects.get(id=oferta_id)
                emails_oferta = o.aplicacion.values_list('email',flat=True)
                if User.objects.get(id = request.POST['usuario']).email in emails_oferta:
                    new = Revisado(oferta = o, usuario = User.objects.get(id=request.POST['usuario']))
                    new.save()
        elif int(request.POST['oferta']) in ofertas_ids2:
            for oferta_id in ofertas_ids2:
                o = Oferta.objects.get(id=oferta_id)
                emails_oferta = o.aplicacion.values_list('email',flat=True)
                if User.objects.get(id = request.POST['usuario']).email in emails_oferta:
                    new = Revisado(oferta = o, usuario = User.objects.get(id=request.POST['usuario']))
                    new.save()
        else:
            o = Oferta.objects.get(id=request.POST['oferta'])
            new = Revisado(oferta = o, usuario = User.objects.get(id=request.POST['usuario']))
            new.save()

        return HttpResponse(status=200)

    def delete(self, request, *args, **kwargs):
        delete = Revisado.objects.filter(oferta = Oferta.objects.get(id=request.POST['oferta']),
                         usuario = User.objects.get(id=request.POST['usuario']))[0].delete()
        return HttpResponse(status=200)



class SeleccionSeleccionadoView(LoginRequiredMixin,
                             mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               generics.GenericAPIView):

    def put(self, request, *args, **kwargs):
        new = Seleccionado(oferta = Oferta.objects.get(id=request.POST['oferta']),
                         usuario = User.objects.get(id=request.POST['usuario']))
        new.save()
        return HttpResponse(status=200)

    def delete(self, request, *args, **kwargs):
        delete = Seleccionado.objects.filter(oferta = Oferta.objects.get(id=request.POST['oferta']),
                         usuario = User.objects.get(id=request.POST['usuario']))[0].delete()
        return HttpResponse(status=200)



class SeleccionView(BaseDatatableView):
    model = User
    columns = ['fullname','departamento','ciudad','titulo','hv','id','email','first_name','last_name',
               'telefono_1','telefono_2','fecha_nacimiento','revisado','seleccionado']
    order_columns = ['fullname','departamento','ciudad','titulo','hv','id','email','first_name','last_name',
                     'telefono_1','telefono_2','fecha_nacimiento','revisado']
    max_display_length = 100

    def render_column(self, row, column):
        if column == 'revisado':
            if(Revisado.objects.filter(usuario__id=row.id,oferta__id=self.kwargs['id_oferta']).count() == 0):
                return "false"
            else:
                return "true"
        if column == 'seleccionado':
            if(Seleccionado.objects.filter(usuario__id=row.id,oferta__id=self.kwargs['id_oferta']).count() == 0):
                return "false"
            else:
                return "true"
        if column == 'fullname':
            return '{0} {1}'.format(row.first_name,row.last_name)
        if column == 'hv':
            try:
                url = row.hv.url
            except:
                url = ""
            return url
        else:
            return super(SeleccionView,self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search == 'revisado':
            aplicados = Oferta.objects.get(id=self.kwargs['id_oferta']).aplicacion.all().values_list('id',flat=True)
            revisados =  Revisado.objects.filter(oferta=Oferta.objects.get(id=self.kwargs['id_oferta']),usuario__id__in=aplicados).values_list('usuario__id',flat=True)
            qs=qs.exclude(id__in=revisados)
        elif search:
            q = Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(departamento__icontains=search) | Q(ciudad__icontains=search) | Q(titulo__icontains=search) | Q(email__icontains=search)
            qs = qs.filter(q)
        return qs

    def get_initial_queryset(self):
        ids_user = Oferta.objects.get(id=self.kwargs['id_oferta']).aplicacion.values_list('id',flat=True)
        return User.objects.filter(id__in=ids_user)