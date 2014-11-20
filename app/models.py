# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

ESTADOS = (
    (0, 'Por Defecto'),
    (1, 'Inactivo'),
    (2, 'Estado2'),
)

TIPOS_REPORTE = (
    (0, 'Ofensivo'),
    (1, 'Ilegal'),
    (2, 'Otros'),
)

NIVELES_MEDALLA = (
    (0, 'Bronce'),
    (1, 'Plata'),
    (2, 'Oro'),
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
    descripcion = models.CharField(max_length=50, default='')
    n_preguntas = models.IntegerField(default=0, verbose_name="Preguntas con este tag")
    def __unicode__(self): return "%s" % (self.nombre)

class comentario(models.Model):
    #pregunta = models.ForeignKey(pregunta)
    #respuesta = models.ForeignKey(respuesta)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    autor = models.ForeignKey(User)
    contenido = models.TextField()
    n_votos = models.IntegerField(default=0)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    fecha_hora = models.DateTimeField(auto_now_add=True)

class pregunta(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    autor = models.ForeignKey(User)
    contenido = models.TextField()
    n_vistas = models.PositiveIntegerField(default=0)
    n_respuestas = models.PositiveIntegerField(default=0)
    n_votos = models.IntegerField(default=0)
    respondido = models.BooleanField(default=False)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(tag, blank=False, related_name='tags')
    comentarios = GenericRelation(comentario)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(pregunta, self).save(*args, **kwargs)

class respuesta(models.Model):
    pregunta = models.ForeignKey(pregunta)
    autor = models.ForeignKey(User)
    contenido = models.TextField()
    n_votos = models.IntegerField(default=0)
    mejor = models.BooleanField(default=False)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    comentarios = GenericRelation(comentario)

class voto(models.Model):
    user = models.ForeignKey(User)
    pregunta = models.ForeignKey(pregunta)
    arriba = models.BooleanField(default=False)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    
class favorito(models.Model):
    user = models.ForeignKey(User)
    pregunta = models.ForeignKey(pregunta)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    
class reporte_usuario(models.Model):
    user = models.ForeignKey(User, related_name='autor')
    reportado = models.ForeignKey(User, related_name='reportado')
    tipo = models.SmallIntegerField(max_length=1, default=0, choices=TIPOS_REPORTE)
    mensaje = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    
class medalla(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    nivel = models.SmallIntegerField(max_length=1, default=0, choices=NIVELES_MEDALLA)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    
class medalla_usuario(models.Model):
    user = models.ForeignKey(User)
    medalla = models.ForeignKey(medalla)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(max_length=1, default=0, choices=ESTADOS)
    