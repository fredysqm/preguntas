# -*- coding: utf-8 -*-

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Button
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions

from django.contrib.auth.models import User
from ..models import pregunta


class pregunta_crear_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(pregunta_crear_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Nueva Pregunta',
                'titulo',
                'contenido',
                'tags',
            ),
            FormActions(
                Submit('submit', u'Guardar Pregunta'),
                css_class='text-right'
            ),
        )

    class Meta:
        model = pregunta
        exclude = ('slug', 'n_vistas', 'n_respuestas', 'n_votos', 'respondido', 'estado', 'autor')


class pregunta_editar_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(pregunta_editar_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Editar Pregunta',
                'titulo',
                'contenido',
                'tags',
            ),
            FormActions(
                Submit('submit', u'Guardar Pregunta'),
                css_class='text-right'
            ),
        )

    class Meta:
        model = pregunta
        exclude = ('slug', 'n_vistas', 'n_respuestas', 'n_votos', 'respondido', 'estado', 'autor')
