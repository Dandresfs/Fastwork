#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from empresa.models import Empresa
from ofertas.models import Oferta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, ButtonHolder, Submit, HTML
from accounts.models import User
import json
import os
from Fastwork.settings import base as settings
from django.utils import timezone


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


class CrearOfertaForm(forms.ModelForm):

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
        super(CrearOfertaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['empresa'].queryset = Empresa.objects.filter(propietario__id = kwargs['initial']['user_id'])
        self.fields['publicacion'].initial = timezone.now()

        if 'data' in kwargs.keys():
            departamentos = json.load(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/municipios.json')))
            choices = self.get_choices(departamentos,*args, **kwargs)
            self.fields['municipio'].widget.choices = choices

        self.helper.layout = Layout(
            Fieldset(
                'Datos principales de la oferta',
                Div(
                    Div(
                        Div('empresa',css_class='col-sm-3'),
                        Div('categoria',css_class='col-sm-4'),
                        Div('titulo',css_class='col-sm-5'),
                        css_class='row'
                    ),
                    Div(
                        Div('departamento',css_class='col-sm-6'),
                        Div('municipio',css_class='col-sm-6'),
                        css_class='row'
                    ),
                    Div(
                        HTML(
                            """
                            <p>*Estos datos no pueden ser editados despues de guardar la oferta.</p>
                            """
                        )
                    ),
                    css_class='col-sm-12'
                ),
            ),
            Fieldset(
                'Información de oferta',
                Div(
                    Div(
                        Div('fecha_contratacion',css_class='col-sm-3'),
                        Div('cierre',css_class='col-sm-3'),
                        Div('vacantes',css_class='col-sm-3'),
                        Div('salario',css_class='col-sm-3'),
                        css_class='row'
                    ),
                    Div(

                        Div('experiencia',css_class='col-sm-3'),
                        Div('educacion',css_class='col-sm-3'),
                        Div('viajar',css_class='col-sm-3 margin-13'),
                        Div('residencia',css_class='col-sm-3 margin-13'),
                        css_class='row'
                    ),
                    Div(
                        Div('descripcion',css_class='col-sm-12'),
                        css_class='row'
                    ),
                    Div(
                        Div('publicacion',css_class='col-sm-12'),
                        css_class='row'
                    ),
                    css_class='col-sm-12'
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Guardar')
            )
        )

    class Meta:
        model = Oferta
        fields = '__all__'
        labels = {'empresa':'Empresa que publica la oferta','titulo':'Titulo de la oferta','cierre':'Fecha de cierre',
                  'fecha_contratacion':'Fecha de contratación','vacantes':'Cantidad de vacantes',
                  'viajar':'Disponibilidad para viajar','residencia':'Disponibilidad para cambiar de residencia',
                  'experiencia':'Años de experiencia','educacion':'Nivel educativo','descripcion':'Descripcion de la oferta'
                  }
        widgets = {
            'publicacion':forms.HiddenInput(),
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
            'municipio': forms.Select(choices= [('','----------')] ),

            'categoria': forms.Select(choices= [('','----------'),
                ('Administración / Oficina','Administración / Oficina'),
                ('Almacén / Logística','Almacén / Logística'),
                ('Atención a clientes','Atención a clientes'),
                ('CallCenter / Telemercadeo','CallCenter / Telemercadeo'),
                ('Compras / Comercio Exterior','Compras / Comercio Exterior'),
                ('Construccion y Obra','Construccion y Obra'),
                ('Contabilidad / Finanzas','Contabilidad / Finanzas'),
                ('Dirección / Gerencia','Dirección / Gerencia'),
                ('Diseño / Artes gráficas','Diseño / Artes gráficas'),
                ('Docencia','Docencia'),
                ('Hostelería / Turismo','Hostelería / Turismo'),
                ('Informática / Telecomunicaciones','Informática / Telecomunicaciones'),
                ('Ingeniería','Ingeniería'),
                ('Investigación y Calidad','Investigación y Calidad'),
                ('Legal / Asesoría','Legal / Asesoría'),
                ('Mantenimiento y Reparaciones Técnicas','Mantenimiento y Reparaciones Técnicas'),
                ('Marketing / Ventas','Marketing / Ventas'),
                ('Medicina / Salud','Medicina / Salud'),
                ('Mercadeo / Publicidad / Comunicación','Mercadeo / Publicidad / Comunicación'),
                ('Producción / Operaciones','Producción / Operaciones'),
                ('Recursos Humanos','Recursos Humanos'),
                ('Servicios Generales, Aseo y Seguridad','Servicios Generales, Aseo y Seguridad'),
            ]),
            'educacion': forms.Select(choices= [('','----------'),
                                                            ('Educación Básica Primaria','Educación Básica Primaria'),
                                                            ('Educación Básica Secundaria','Educación Básica Secundaria'),
                                                            ('Bachillerato / Educación Media','Bachillerato / Educación Media'),
                                                            ('Universidad / Carrera técnica','Universidad / Carrera técnica'),
                                                            ('Universidad / Carrera tecnológica','Universidad / Carrera tecnológica'),
                                                            ('Universidad / Carrera Profesional','Universidad / Carrera Profesional'),
                                                            ('Postgrado / Especialización','Postgrado / Especialización'),
                                                            ('Postgrado / Maestría','Postgrado / Maestría'),
                                                            ('Postgrado / Doctorado','Postgrado / Doctorado'),
            ] ),
        }


class UpdateEmpresaForm(forms.ModelForm):

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

    def get_choices_string(self,json,departamento,*args, **kwargs):
        response = [('', '----------')]
        x = departamento
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
        super(UpdateEmpresaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        departamentos = json.load(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/municipios.json')))

        choices = self.get_choices_string(departamentos,kwargs['instance'].departamento,*args, **kwargs)
        self.fields['ciudad'].widget.choices = choices

        if 'data' in kwargs.keys():
            choices = self.get_choices(departamentos,*args, **kwargs)
            self.fields['ciudad'].widget.choices = choices

        self.helper.layout = Layout(
            Fieldset(
                'Datos de la empresa',
                Div(
                    Div(
                        HTML(
                        """
                        <div class='col-sm-12'><p>Nombre comercial: {{nombre_comercial}}</p></div>
                        <div class='col-sm-12'><p>Razón social: {{razon_social}}</p></div>
                        """
                        ),
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
        exclude = ['propietario','nombre_comercial','razon_social']
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


class UpdateOfertaForm(forms.ModelForm):

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
        super(UpdateOfertaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Datos principales de la oferta',
                Div(
                    Div(
                        HTML("""
                        <p><b>Empresa:</b>  {{empresa}}</p>
                        <p><b>Categoria:</b>  {{categoria}}</p>
                        <p><b>Titulo:</b>  {{titulo}}</p>
                        <p><b>Departamento:</b>  {{departamento}}</p>
                        <p><b>Municipio:</b>  {{municipio}}</p>
                        """),
                        css_class='row'
                    ),
                    css_class='col-sm-12'
                ),
            ),
            Fieldset(
                'Información de oferta',
                Div(
                    Div(
                        Div('fecha_contratacion',css_class='col-sm-3'),
                        Div('cierre',css_class='col-sm-3'),
                        Div('vacantes',css_class='col-sm-3'),
                        Div('salario',css_class='col-sm-3'),
                        css_class='row'
                    ),
                    Div(

                        Div('experiencia',css_class='col-sm-3'),
                        Div('educacion',css_class='col-sm-3'),
                        Div('viajar',css_class='col-sm-3 margin-13'),
                        Div('residencia',css_class='col-sm-3 margin-13'),
                        css_class='row'
                    ),
                    Div(
                        Div('descripcion',css_class='col-sm-12'),
                        css_class='row'
                    ),
                    Div(
                        Div('publicacion',css_class='col-sm-12'),
                        css_class='row'
                    ),
                    css_class='col-sm-12'
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Guardar')
            )
        )

    class Meta:
        model = Oferta
        exclude = ['empresa','categoria','titulo','departamento','municipio']
        labels = {'empresa':'Empresa que publica la oferta','titulo':'Titulo de la oferta','cierre':'Fecha de cierre',
                  'fecha_contratacion':'Fecha de contratación','vacantes':'Cantidad de vacantes',
                  'viajar':'Disponibilidad para viajar','residencia':'Disponibilidad para cambiar de residencia',
                  'experiencia':'Años de experiencia','educacion':'Nivel educativo','descripcion':'Descripcion de la oferta'
                  }
        widgets = {
            'publicacion':forms.HiddenInput(),
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
            'municipio': forms.Select(choices= [('','----------')] ),

            'categoria': forms.Select(choices= [('','----------'),
                ('Administración / Oficina','Administración / Oficina'),
                ('Almacén / Logística','Almacén / Logística'),
                ('Atención a clientes','Atención a clientes'),
                ('CallCenter / Telemercadeo','CallCenter / Telemercadeo'),
                ('Compras / Comercio Exterior','Compras / Comercio Exterior'),
                ('Construccion y Obra','Construccion y Obra'),
                ('Contabilidad / Finanzas','Contabilidad / Finanzas'),
                ('Dirección / Gerencia','Dirección / Gerencia'),
                ('Diseño / Artes gráficas','Diseño / Artes gráficas'),
                ('Docencia','Docencia'),
                ('Hostelería / Turismo','Hostelería / Turismo'),
                ('Informática / Telecomunicaciones','Informática / Telecomunicaciones'),
                ('Ingeniería','Ingeniería'),
                ('Investigación y Calidad','Investigación y Calidad'),
                ('Legal / Asesoría','Legal / Asesoría'),
                ('Mantenimiento y Reparaciones Técnicas','Mantenimiento y Reparaciones Técnicas'),
                ('Marketing / Ventas','Marketing / Ventas'),
                ('Medicina / Salud','Medicina / Salud'),
                ('Mercadeo / Publicidad / Comunicación','Mercadeo / Publicidad / Comunicación'),
                ('Producción / Operaciones','Producción / Operaciones'),
                ('Recursos Humanos','Recursos Humanos'),
                ('Servicios Generales, Aseo y Seguridad','Servicios Generales, Aseo y Seguridad'),
            ]),
            'educacion': forms.Select(choices= [('','----------'),
                                                            ('Educación Básica Primaria','Educación Básica Primaria'),
                                                            ('Educación Básica Secundaria','Educación Básica Secundaria'),
                                                            ('Bachillerato / Educación Media','Bachillerato / Educación Media'),
                                                            ('Universidad / Carrera técnica','Universidad / Carrera técnica'),
                                                            ('Universidad / Carrera tecnológica','Universidad / Carrera tecnológica'),
                                                            ('Universidad / Carrera Profesional','Universidad / Carrera Profesional'),
                                                            ('Postgrado / Especialización','Postgrado / Especialización'),
                                                            ('Postgrado / Maestría','Postgrado / Maestría'),
                                                            ('Postgrado / Doctorado','Postgrado / Doctorado'),
            ] ),
        }


class ComprarCreditoEmpresaForm(forms.Form):

    cantidad = forms.IntegerField(widget=forms.Select(choices = [('','----------'),
                                                                 ('1','1 Credito'),
                                                                 ('2','2 Creditos'),
                                                                 ('3','3 Creditos'),
                                                                 ('4','4 Creditos'),
                                                                 ('5','5 Creditos'),] ))
    nombres = forms.CharField(max_length=256,required=True)
    apellidos = forms.CharField(max_length=256,required=True)
    cedula = forms.IntegerField()
    direccion = forms.CharField(max_length=256,required=True)
    telefono = forms.CharField(max_length=256,required=True)

    def __init__(self, *args, **kwargs):
        super(ComprarCreditoEmpresaForm, self).__init__(*args, **kwargs)

        user = User.objects.get(id = kwargs['initial']['user_id'])

        self.helper = FormHelper(self)

        self.fields['nombres'].initial = user.first_name
        self.fields['apellidos'].initial = user.last_name

        self.helper.layout = Layout(
            Fieldset(
                'Información para factura',
                Div(
                    Div(
                        'nombres',
                        css_class='col-sm-4'
                    ),
                    Div(
                        'apellidos',
                        css_class='col-sm-4'
                    ),
                    Div(
                        'cedula',
                        css_class='col-sm-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        'direccion',
                        css_class='col-sm-6'
                    ),
                    Div(
                        'telefono',
                        css_class='col-sm-6'
                    ),
                    css_class='row'
                ),
            ),
            Fieldset(
                'Creditos',
                Div(
                    Div(
                        'cantidad',
                        css_class='col-sm-6'
                    ),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Guardar')
            )
        )


class ComprarCreditoOfertaForm(forms.Form):

    cantidad_oferta = forms.IntegerField(widget=forms.Select(choices = [('','----------'),
                                                                 ('1','1 Credito'),
                                                                 ('2','2 Creditos'),
                                                                 ('3','3 Creditos'),
                                                                 ('4','4 Creditos'),
                                                                 ('5','5 Creditos'),] ))
    nombres_oferta = forms.CharField(max_length=256,required=True)
    apellidos_oferta = forms.CharField(max_length=256,required=True)
    cedula_oferta = forms.IntegerField()
    direccion_oferta = forms.CharField(max_length=256,required=True)
    telefono_oferta = forms.CharField(max_length=256,required=True)

    def __init__(self, *args, **kwargs):
        super(ComprarCreditoOfertaForm, self).__init__(*args, **kwargs)

        user = User.objects.get(id = kwargs['initial']['user_id'])

        self.helper = FormHelper(self)

        self.fields['nombres_oferta'].initial = user.first_name
        self.fields['apellidos_oferta'].initial = user.last_name

        self.helper.layout = Layout(
            Fieldset(
                'Información para factura',
                Div(
                    Div(
                        'nombres_oferta',
                        css_class='col-sm-4'
                    ),
                    Div(
                        'apellidos_oferta',
                        css_class='col-sm-4'
                    ),
                    Div(
                        'cedula_oferta',
                        css_class='col-sm-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        'direccion_oferta',
                        css_class='col-sm-6'
                    ),
                    Div(
                        'telefono_oferta',
                        css_class='col-sm-6'
                    ),
                    css_class='row'
                ),
            ),
            Fieldset(
                'Creditos',
                Div(
                    Div(
                        'cantidad_oferta',
                        css_class='col-sm-6'
                    ),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Guardar')
            )
        )