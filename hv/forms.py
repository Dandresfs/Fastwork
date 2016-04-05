#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from accounts.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, ButtonHolder, Submit, HTML


class ProfesionalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfesionalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos Profesionales',
                Div(
                    Div('titulo',css_class='col-sm-12'),
                    Div('perfil',css_class='col-sm-12'),
                ),
            ),
            Fieldset(
                'Experiencias profesionales',
                Div(css_class='experiencias row',
                ),
                Div(
                    HTML("""
                        <button type="button" class="btn btn-success pull-right margin-div" data-toggle="modal" data-target="#ExperienciaModal">
                          Añadir Experiencia
                        </button>
                    """),
                )
            ),
            Fieldset(
                'Formación',
                Div(css_class='formaciones row',
                ),
                Div(
                    HTML("""
                        <button type="button" class="btn btn-success pull-right margin-div" data-toggle="modal" data-target="#FormacionModal">
                          Añadir Formación
                        </button>
                    """),
                )
            ),

            Fieldset(
                'Hoja de Vida',
                'hv'
            ),

            ButtonHolder(
                Submit('submit', 'Guardar')
            )
        )

    class Meta:
        model = User
        fields = ['titulo','perfil','hv']
        labels = {
            'titulo': 'Titulo*',
            'perfil': 'Descripción breve de su perfil profesional*',
            'hv': 'Hoja de vida.'
        }