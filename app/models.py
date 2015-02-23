# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

ESTADO = (
    (0, 'default'),
    (1, 'pendiente'),
    (2, 'eliminado'),
)

REPORTE = (
    (0, 'ofensivo'),
    (1, 'ilegal'),
    (2, 'otros'),
)

class usuario_extra(models.Model):
    usuario_extra = models.OneToOneField(User, primary_key=True)
    puntaje = models.IntegerField(default=0, verbose_name="Puntaje")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción", blank=True)

class tag(models.Model):
    nombre = models.CharField(max_length=25)
    slug = models.SlugField(max_length=25)
    def __unicode__(self): return "%s" % (self.nombre)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(tag, self).save(*args, **kwargs)

class pregunta(models.Model):
    autor = models.ForeignKey(User)
    titulo = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    contenido = models.TextField()
    n_vistas = models.PositiveIntegerField(default=0)
    n_respuestas = models.PositiveIntegerField(default=0)
    n_votos = models.IntegerField(default=0)
    tags = models.ManyToManyField(tag)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): return "%s" % (self.titulo)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(pregunta, self).save(*args, **kwargs)

class respuesta(models.Model):
    pregunta = models.ForeignKey(pregunta)
    autor = models.ForeignKey(User)
    contenido = models.TextField()
    n_votos = models.IntegerField(default=0)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)
    fecha_hora = models.DateTimeField(auto_now_add=True)