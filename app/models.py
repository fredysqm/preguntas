# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

ESTADOS = (
    (0, 'Por Detecto'),
    (1, 'Estado1'),
    (2, 'Estado2'),
)

class usuario_extra(models.Model):
    usuario_extra = models.OneToOneField(User, primary_key=True)
    rol = models.CharField(max_length=1, verbose_name="Rol")
    puntaje = models.IntegerField(default=0, verbose_name="Puntaje")

class usuario_detalles(models.Model):
    usuario_detalles = models.OneToOneField(User, primary_key=True)
    descripcion = models.CharField(max_length=255, verbose_name="Descripción", blank=True)

class tag(models.Model):
    nombre = models.CharField(max_length=25)

class pregunta(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(User)
    contenido = models.TextField()
    n_vistas = models.PositiveIntegerField(default=0)
    n_respuestas = models.PositiveIntegerField(default=0)
    n_votos = models.IntegerField(default=0)
    respondido = models.BooleanField(default=False)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(tag)

class respuesta(models.Model):
    pregunta = models.ForeignKey(pregunta)
    autor = models.ForeignKey(User)
    contenido = models.TextField()
    n_votos = models.IntegerField(default=0)
    mejor = models.BooleanField(default=False)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    fecha_hora = models.DateTimeField(auto_now_add=True)

class comentario(models.Model):
    pregunta = models.ForeignKey(pregunta)
    respuesta = models.ForeignKey(respuesta)
    autor = models.ForeignKey(User)
    contenido = models.TextField()
    n_votos = models.IntegerField(default=0)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    fecha_hora = models.DateTimeField(auto_now_add=True)
