from django import forms
from django.contrib.auth.models import User
from .models import pregunta, respuesta, tag, comentario

class pregunta_form(forms.ModelForm):
    class Meta:
        model = pregunta
        exclude = ()

class pregunta_eliminar_form(forms.ModelForm):
    class Meta:
        model = pregunta
        exclude = ()
        
class user_form(forms.ModelForm):
    class Meta:
        model = User
        exclude = ()

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