#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, ButtonHolder, Submit

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Cuenta de usuario',
                Div(
                    Div('fullname',css_class='col-md-6'),
                    Div('username',css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Datos Personales',
                Div(
                    Div('first_name',css_class='col-md-6'),
                    Div('last_name',css_class='col-md-6'),
                ),
                Div(
                    Div('tipo_identificacion',css_class='col-md-4'),
                    Div('identificacion',css_class='col-md-4'),
                    Div('fecha_nacimiento',css_class='col-md-4'),
                ),
                Div(
                    Div('genero',css_class='col-md-3'),
                    Div('estado_civil',css_class='col-md-3'),
                    Div('telefono_1',css_class='col-md-3'),
                    Div('telefono_2',css_class='col-md-3'),
                ),
                Div(
                    Div('departamento',css_class='col-md-4'),
                    Div('ciudad',css_class='col-md-4'),
                    Div('direccion',css_class='col-md-4'),
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
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'fullname': 'Nombre completo',
            'tipo_identificacion': 'Tipo de identificación',
            'identificacion': 'identificación',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'telefono_1': 'Teléfono',
            'telefono_2': 'Teléfono alternativo',
        }
        widgets = {
            'tipo_identificacion': forms.Select(choices=(('----------', '----------'),
                                                         ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
                                                         ('Cédula de extranjería', 'Cédula de extranjería'),
                                                         ('Tarjeta de identidad', 'Tarjeta de identidad'),
                                                         ('Pasaporte', 'Pasaporte'),
                                                         ('Número de Identificación', 'Número de Identificación'),)),
            'genero': forms.Select(choices=(('----------', '----------'),
                                            ('Masculino', 'Masculino'),
                                            ('Femenino', 'Femenino'),)),

            'estado_civil': forms.Select(choices=(('----------', '----------'),
                                            ('Soltero(a)', 'Soltero(a)'),
                                            ('Casado(a)', 'Casado(a)'),
                                            ('Divorciado(a)', 'Divorciado(a)'),
                                            ('Viudo(a)', 'Viudo(a)'),)),
        }