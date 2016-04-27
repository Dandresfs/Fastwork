#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import User, PreUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, ButtonHolder, Submit
import json
import os
from Fastwork.settings import base as settings

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class AccountForm(forms.ModelForm):

    def get_choices(self,json,*args, **kwargs):
        response = [('', '----------')]
        try:
            list = json[kwargs['instance'].departamento]
        except KeyError:
            return response
        else:
            for item in list:
                response.append(tuple([item.encode('utf-8'),item.encode('utf-8')]))
            response = sorted(response, key=lambda x: x[0])
            return response


    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        departamentos = json.load(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/municipios.json')))
        choices = self.get_choices(departamentos,*args, **kwargs)
        self.Meta.widgets['ciudad'].choices = choices
        self.fields['ciudad'].widget.choices = choices
        self.helper.layout = Layout(
            Fieldset(
                'Cuenta de Usuario',
                Div(
                    Div('fullname',css_class='col-sm-6'),
                    Div('username',css_class='col-sm-6'),
                ),
            ),
            Fieldset(
                'Datos Personales',
                Div(
                    Div('first_name',css_class='col-sm-6'),
                    Div('last_name',css_class='col-sm-6'),
                ),
                Div(
                    Div('tipo_identificacion',css_class='col-md-4 col-sm-6'),
                    Div('identificacion',css_class='col-md-4 col-sm-6'),
                    Div('fecha_nacimiento',css_class='col-md-4 col-sm-6'),
                ),
                Div(
                    Div('genero',css_class='col-md-3 col-sm-6'),
                    Div('estado_civil',css_class='col-md-3 col-sm-6'),
                    Div('telefono_1',css_class='col-md-3 col-sm-6'),
                    Div('telefono_2',css_class='col-md-3 col-sm-6'),
                )
            ),
            Fieldset(
                'Residencia',
                Div(
                    Div('departamento',css_class='col-md-4 col-sm-6'),
                    Div('ciudad',css_class='col-md-4 col-sm-6'),
                    Div('direccion',css_class='col-md-4 col-sm-6'),
                )
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white')
            )
        )

    class Meta:
        model = User
        fields = ['tipo_identificacion','fullname','username','first_name','last_name','identificacion','fecha_nacimiento',
                  'genero','estado_civil','telefono_1','telefono_2','departamento','ciudad','direccion']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'fullname': 'Nombre completo',
            'tipo_identificacion': 'Tipo de identificación*',
            'identificacion': 'Identificación*',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'telefono_1': 'Celular*',
            'telefono_2': 'Teléfono alternativo',
            'departamento': 'Departamento*',
            'ciudad': 'Ciudad*',
            'direccion': 'Dirección',
            'genero': 'Genero*',
            'estado_civil': 'Estado civil*',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'required':'required'}),
            'last_name': forms.TextInput(attrs={'required':'required'}),
            'identificacion': forms.NumberInput(attrs={'required':'required'}),
            'telefono_1': forms.NumberInput(attrs={'required':'required'}),
            'tipo_identificacion': forms.Select(attrs={'required':'required'},choices=(('', '----------'),
                                                         ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
                                                         ('Cédula de extranjería', 'Cédula de extranjería'),
                                                         ('Tarjeta de identidad', 'Tarjeta de identidad'),
                                                         ('Pasaporte', 'Pasaporte'),
                                                         ('Número de Identificación', 'Número de Identificación'),)),
            'genero': forms.Select(attrs={'required':'required'},choices=(('', '----------'),
                                            ('Masculino', 'Masculino'),
                                            ('Femenino', 'Femenino'),)),

            'estado_civil': forms.Select(attrs={'required':'required'},choices=(('', '----------'),
                                            ('Soltero(a)', 'Soltero(a)'),
                                            ('Casado(a)', 'Casado(a)'),
                                            ('Divorciado(a)', 'Divorciado(a)'),
                                            ('Viudo(a)', 'Viudo(a)'),)),
            'departamento': forms.Select(attrs={'required':'required'},choices=(('', '----------'),
                                            ('Amazonas', 'Amazonas'),
                                            ('Antioquia', 'Antioquia'),
                                            ('Arauca', 'Arauca'),
                                            ('Atlántico', 'Atlántico'),
                                            ('Bolívar', 'Bolívar'),
                                            ('Boyacá', 'Boyacá'),
                                            ('Caldas', 'Caldas'),
                                            ('Caquetá', 'Caquetá'),
                                            ('Casanare', 'Casanare'),
                                            ('Cauca', 'Cauca'),
                                            ('Cesar', 'Cesar'),
                                            ('Chocó', 'Chocó'),
                                            ('Córdoba', 'Córdoba'),
                                            ('Cundinamarca', 'Cundinamarca'),
                                            ('Guainía', 'Guainía'),
                                            ('Guaviare', 'Guaviare'),
                                            ('Huila', 'Huila'),
                                            ('La Guajira', 'La Guajira'),
                                            ('Magdalena', 'Magdalena'),
                                            ('Meta', 'Meta'),
                                            ('Nariño', 'Nariño'),
                                            ('Norte de Santander', 'Norte de Santander'),
                                            ('Putumayo', 'Putumayo'),
                                            ('Quindío', 'Quindío'),
                                            ('Risaralda', 'Risaralda'),
                                            ('San Andrés y Providencia', 'San Andrés y Providencia'),
                                            ('Santander', 'Santander'),
                                            ('Sucre', 'Sucre'),
                                            ('Tolima', 'Tolima'),
                                            ('Valle del Cauca', 'Valle del Cauca'),
                                            ('Vaupés', 'Vaupés'),
                                            ('Vichada', 'Vichada'),
                                        )),

            'ciudad': forms.Select(attrs={'required':'required'},choices=(('', '----------'),
                                            )),
        }