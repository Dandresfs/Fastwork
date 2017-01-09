#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from empresa.models import Empresa
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, ButtonHolder, Submit, HTML
from accounts.models import User
import json
import os
from Fastwork.settings import base as settings


class CrearEmpresaForm(forms.ModelForm):

    def get_choices(self,json,*args, **kwargs):
        response = [('', '----------')]
        x = kwargs['data']['departamento']
        try:
            list = json[x]
        except KeyError:
            return response
        else:
            for item in list:
                response.append(tuple([item,item]))
            response = sorted(response, key=lambda x: x[0])
            return response

    def __init__(self, *args, **kwargs):
        super(CrearEmpresaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['propietario'].initial = User.objects.get(id = kwargs['initial']['user_id'])

        if 'data' in kwargs.keys():
            departamentos = json.load(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/municipios.json')))
            choices = self.get_choices(departamentos,*args, **kwargs)
            self.fields['ciudad'].widget.choices = choices

        self.helper.layout = Layout(
            Fieldset(
                'Datos de la empresa',
                Div(
                    Div(
                        Div('propietario',css_class='col-sm-0'),
                        Div('nombre_comercial',css_class='col-sm-6'),
                        Div('razon_social',css_class='col-sm-6'),
                    ),
                    Div(
                        Div('nit',css_class='col-sm-4'),
                        Div('departamento',css_class='col-sm-4'),
                        Div('ciudad',css_class='col-sm-4'),
                    ),
                    Div(
                        Div('direccion',css_class='col-sm-4'),
                        Div('sector',css_class='col-sm-4'),
                        Div('cantidad_trabajadores',css_class='col-sm-4'),
                    ),
                    css_class='col-sm-12'
                ),
            ),
            Fieldset(
                'Tipo de empresa',
                Div(
                    Div(
                        Div('tipo',css_class='col-sm-12'),
                        Div('descripcion',css_class='col-sm-12'),
                        Div('pagina_web',css_class='col-sm-12'),
                        Div('logo',css_class='col-sm-12'),
                    ),
                    css_class='col-sm-12'
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Guardar')
            )
        )

    class Meta:
        model = Empresa
        fields = '__all__'
        labels = {'direccion':'Dirección','cantidad_trabajadores':'Cantidad de trabajadores','tipo':'Tipologia',
                  'descripcion':'Descripción','pagina_web':'Página web'}
        widgets = {
            'propietario':forms.HiddenInput(),
            'departamento':forms.Select(choices=[
                                                    ('','----------'),
                                                    ('Amazonas','Amazonas'),
                                                    ('Antioquia','Antioquia'),
                                                    ('Arauca','Arauca'),
                                                    ('Atlántico','Atlántico'),
                                                    ('Bolívar','Bolívar'),
                                                    ('Boyacá','Boyacá'),
                                                    ('Caldas','Caldas'),
                                                    ('Caquetá','Caquetá'),
                                                    ('Casanare','Casanare'),
                                                    ('Cauca','Cauca'),
                                                    ('Cesar','Cesar'),
                                                    ('Chocó','Chocó'),
                                                    ('Córdoba','Córdoba'),
                                                    ('Cundinamarca','Cundinamarca'),
                                                    ('Guainía','Guainía'),
                                                    ('Guaviare','Guaviare'),
                                                    ('Huila','Huila'),
                                                    ('La Guajira','La Guajira'),
                                                    ('Magdalena','Magdalena'),
                                                    ('Meta','Meta'),
                                                    ('Nariño','Nariño'),
                                                    ('Norte de Santander','Norte de Santander'),
                                                    ('Putumayo','Putumayo'),
                                                    ('Quindío','Quindío'),
                                                    ('Risaralda','Risaralda'),
                                                    ('San Andrés y Providencia','San Andrés y Providencia'),
                                                    ('Santander','Santander'),
                                                    ('Sucre','Sucre'),
                                                    ('Tolima','Tolima'),
                                                    ('Valle del Cauca','Valle del Cauca'),
                                                    ('Vaupés','Vaupés'),
                                                    ('Vichada','Vichada'),
            ]),
            'ciudad': forms.Select(choices= [('','----------')] ),
            'sector': forms.Select(choices= [('','----------'),
                ('Agricultura / Pesca / Ganadería<','Agricultura / Pesca / Ganadería'),
                ('Construcción / obras','Construcción / obras'),
                ('Educación','Educación'),
                ('Energía','Energía'),
                ('Entretenimiento / Deportes','Entretenimiento / Deportes'),
                ('Fabricación','Fabricación'),
                ('Finanzas / Banca','Finanzas / Banca'),
                ('Gobierno / No Lucro','Gobierno / No Lucro'),
                ('Hostelería / Turismo','Hostelería / Turismo'),
                ('Informática / Hardware','Informática / Hardware'),
                ('Informática / Software','Informática / Software'),
                ('Internet','Internet'),
                ('Legal / Asesoría','Legal / Asesoría'),
                ('Materias Primas','Materias Primas'),
                ('Medios de Comunicación','Medios de Comunicación'),
                ('Publicidad / RRPP','Publicidad / RRPP'),
                ('RRHH / Personal','RRHH / Personal'),
                ('Salud / Medicina','Salud / Medicina'),
                ('Servicios Profesionales','Servicios Profesionales'),
                ('Telecomunicaciones','Telecomunicaciones'),
                ('Transporte','Transporte'),
                ('Venta al consumidor','Venta al consumidor'),
                ('Venta al por mayor','Venta al por mayor'),
            ]),
            'cantidad_trabajadores': forms.Select(choices= [('','----------'),
                                                            ('De 1 a 5 trabajadores','De 1 a 5 trabajadores'),
                                                            ('De 6 a 10 trabajadores','De 6 a 10 trabajadores'),
                                                            ('De 11 a 50 trabajadores','De 11 a 50 trabajadores'),
                                                            ('De 51 a 100 trabajadores','De 51 a 100 trabajadores'),
                                                            ('De 101 a 250 trabajadores','De 101 a 250 trabajadores'),
                                                            ('De 251 a 500 trabajadores','De 251 a 500 trabajadores'),
                                                            ('Más de 501 trabajadores','Más de 501 trabajadores')
            ] ),
            'tipo': forms.Select(choices= [('','----------'),
                                           ('Empleador directo','Empleador directo'),
                                           ('Agencia de reclutamiento','Agencia de reclutamiento'),
                                           ('Servicios temporales','Servicios temporales'),
            ]),
        }