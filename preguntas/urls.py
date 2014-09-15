from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',
    url(r'^$', 'home_view', name='home_url'),

    url(r'^preguntas/$', 'preguntas_view', name='preguntas_url'),
    url(r'^preguntas/crear/$', 'preguntas_crear_view', name='preguntas_crear_url'),
    url(r'^preguntas/(\d+)/responder/$', 'preguntas_responder_view', name='preguntas_responder_url'),




    #url(r'^preguntas/$', 'preguntas_view', name='preguntas_url'),

    #url(r'^preguntas/(?P<id>[-\w]+)/$', 'pregunta_simple'),

    #url(r'^tags/$', 'tags'),

    #url(r'^users/$', 'usuarios'),




    #url(r'^crear/usuario$', 'crear_usuario'),

    #url(r'^crear/respuesta$', 'crear_respuesta'),

    #url(r'^crear/tag$', 'crear_tag'),


    #url(r'^listar/preguntas$', 'listar_preguntas'),


    #url(r'^responder/([0-9]+)$', 'responder_pregunta'),
    #url(r'^exito/respuesta$', 'respuesta_creada'),

    url(r'^admin/', include(admin.site.urls)),
)
