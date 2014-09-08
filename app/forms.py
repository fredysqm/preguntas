from django import forms
from models import Pregunta, Respuesta, Tag
from django.contrib.auth.models import User

class PreguntaForm(forms.ModelForm): 
    class Meta:
        model = Pregunta

class UserForm(forms.ModelForm): 
    class Meta:
        model = User
        
class RespuestaForm(forms.ModelForm): 
    class Meta:
        model = Respuesta
        
class TagForm(forms.ModelForm): 
    class Meta:
        model = Tag