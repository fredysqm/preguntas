# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Button
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions

from .models import pregunta, respuesta, tag, comentario, usuario_detalles

class pregunta_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(pregunta_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Crear Pregunta',
                'titulo',
                'contenido',
                'tags',
            ),
            FormActions(
                Submit('submit', u'Crear'),
                css_class='text-right'
            ),
        )

    class Meta:
        model = pregunta
        exclude = ('n_vistas', 'n_respuestas', 'n_votos', 'respondido', 'estado', 'autor', 'slug')


class pregunta_eliminar_form(forms.ModelForm):
    class Meta:
        model = pregunta
        exclude = ()

class user_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email',)

class user_editar_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)
        
class user_detalles_form(forms.ModelForm):
    class Meta:
        model = usuario_detalles
        fields = ('descripcion',)
        
class respuesta_form(forms.ModelForm):
    class Meta:
        model = respuesta
        exclude = ()

class respuesta_eliminar_form(forms.ModelForm):
    class Meta:
        model = respuesta
        exclude = ()

class tag_form(forms.ModelForm):
    class Meta:
        model = tag
        exclude = ()

class comentario_form(forms.ModelForm):
    class Meta:
        model = comentario
        exclude = ()

class comentario_eliminar_form(forms.ModelForm):
    class Meta:
        model = comentario
        exclude = ()