from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import *

urlpatterns = patterns('',
    # home
    url(r'^$', 'app.views.index'),
    # preguntas
    url(r'^preguntas/', 'app.views.preguntas'),
    # pregunta simple
    url(r'^preguntas/(?P<id>[-\w]+)/$', 'app.views.pregunta_simple'),
    # tags
    url(r'^tags/', 'app.views.tags'),
    # usuarios
    url(r'^users/', 'app.views.usuarios'),
    
    # crear pregunta
    url(r'^crear/pregunta', 'app.views.crear_pregunta'),
    # crear usuario
    url(r'^crear/usuario', 'app.views.crear_usuario'),
    # crear respeusta
    url(r'^crear/respuesta', 'app.views.crear_respuesta'),
    # crear tag
    url(r'^crear/tag', 'app.views.crear_tag'),
)
