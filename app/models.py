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

MEDALLA = (
    (0, 'bronce'),
    (1, 'plata'),
    (2, 'oro'),
)

class usuario_extra(models.Model):
    usuario_extra = models.OneToOneField(User, primary_key=True)
    rol = models.CharField(max_length=1, verbose_name="Rol")
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
    titulo = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
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

class contenido(models.Model):
    pregunta = models.ForeignKey(pregunta)
    autor = models.ForeignKey(User)
    texto = models.TextField()
    n_votos = models.IntegerField(default=0)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)
    fecha_hora = models.DateTimeField(auto_now_add=True)

class comentario(models.Model):
    contenido = models.ForeignKey(contenido)
    autor = models.ForeignKey(User)
    texto = models.TextField()
    n_votos = models.IntegerField(default=0)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)
    fecha_hora = models.DateTimeField(auto_now_add=True)

class voto(models.Model):
    user = models.ForeignKey(User)
    pregunta = models.ForeignKey(pregunta)
    valor = models.SmallIntegerField(default=1)

class favorito(models.Model):
    user = models.ForeignKey(User)
    pregunta = models.ForeignKey(pregunta)

class usuario_reporte(models.Model):
    user = models.ForeignKey(User, related_name='autor')
    reportado = models.ForeignKey(User, related_name='reportado')
    tipo = models.SmallIntegerField(max_length=1, default=0, choices=REPORTE)
    mensaje = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)

class contenido_reporte(models.Model):
    user = models.ForeignKey(User)
    contenido = models.ForeignKey(contenido)
    tipo = models.SmallIntegerField(max_length=1, default=0, choices=REPORTE)
    mensaje = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)

class medalla(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    nivel = models.SmallIntegerField(max_length=1, default=0, choices=MEDALLA)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)

class usuario_medalla(models.Model):
    user = models.ForeignKey(User)
    medalla = models.ForeignKey(medalla)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADO)
