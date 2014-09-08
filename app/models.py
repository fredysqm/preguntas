from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class UserDetalles(models.Model):
    id = models.OneToOneField( User, primary_key=True )
    first_name = models.CharField( max_length=50 )
    last_name = models.CharField( max_length=50 )
    rol = models.CharField( max_length=1 )
    fecha_registro = models.DateField( auto_now_add=True )
    fecha_movimento = models.DateField( auto_now_add=True )
    descripcion = models.CharField( max_length=100 )
    puntaje = models.IntegerField( default=0 )

class Tag(models.Model):
    id = models.AutoField( primary_key=True )
    nombre = models.CharField( max_length=25 )
    
class Pregunta(models.Model):
    id = models.AutoField( primary_key=True )
    titulo = models.CharField( max_length=100 )
    autor = models.ForeignKey( User )
    contenido = models.TextField()
    n_vistas = models.PositiveIntegerField( default=0 )
    n_respuestas = models.PositiveIntegerField( default=0 )
    n_votos = models.IntegerField( default=0 )
    respondido = models.BooleanField( default=False )
    estado = models.CharField( max_length=2 )
    fecha_hora = models.DateField( auto_now_add=True )

class Respuesta(models.Model):
    id = models.AutoField( primary_key=True )
    pregunta_id = models.ForeignKey( Pregunta )
    autor = models.CharField( max_length=20 )
    contenido = models.TextField()
    n_votos = models.IntegerField( default=0 )
    mejor = models.BooleanField( default=False )
    estado = models.CharField( max_length=2 )
    fecha_hora = models.DateField( auto_now_add=True )

class Comentario(models.Model):
    id = models.AutoField( primary_key=True )
    id_pregunta = models.ForeignKey( Pregunta )
    id_respuesta = models.ForeignKey( Respuesta )
    autor = models.CharField( max_length=20 )
    contenido = models.TextField()
    n_votos = models.IntegerField( default=0 )
    estado = models.CharField( max_length=2 )
    fecha_hora = models.DateField( auto_now_add=True )
