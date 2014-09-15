from django import forms
from django.contrib.auth.models import User
from .models import pregunta, respuesta, tag

class pregunta_form(forms.ModelForm):
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

class tag_form(forms.ModelForm):
    class Meta:
        model = tag
        exclude = ()