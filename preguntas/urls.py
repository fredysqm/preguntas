from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',
    url(r'^$', 'home_view', name='home_url'),

    url(r'^preguntas/$', 'preguntas_view', name='preguntas_url'),
    url(r'^preguntas/crear/$', 'preguntas_crear_view', name='preguntas_crear_url'),
    url(r'^preguntas/(\d+)/editar/$', 'preguntas_editar_view', name='preguntas_editar_url'),
    url(r'^preguntas/(\d+)/eliminar/$', 'preguntas_eliminar_view', name='preguntas_eliminar_url'),
    url(r'^preguntas/(\d+)/responder/$', 'preguntas_responder_view', name='preguntas_responder_url'),

    url(r'^preguntas/tagged/(\d+)/$', 'preguntas_tagged_view', name='preguntas_tagged_url'),
    #Preguntas sin responder
    url(r'^preguntas/abiertas/$', 'preguntas_abiertas_view', name='preguntas_abiertas_url'),


    #url(r'^preguntas/$', 'preguntas_view', name='preguntas_url'),

    #url(r'^preguntas/(?P<id>[-\w]+)/$', 'pregunta_simple'),

    #url(r'^tags/$', 'tags'),

    #url(r'^users/$', 'usuarios'),




    #url(r'^crear/usuario$', 'crear_usuario'),

    #url(r'^crear/respuesta$', 'crear_respuesta'),

    url(r'^respuestas/(\d+)/editar$', 'respuestas_editar_view', name='respuestas_editar_url'),
    url(r'^respuestas/(\d+)/eliminar$', 'respuestas_eliminar_view', name='respuestas_eliminar_url'),
    
    url(r'^tags/crear/$', 'tags_crear_view', name='tags_crear_url'),


    #url(r'^listar/preguntas$', 'listar_preguntas'),


    #url(r'^responder/([0-9]+)$', 'responder_pregunta'),
    #url(r'^exito/respuesta$', 'respuesta_creada'),

    url(r'user/(\d+)/$', 'usuarios_perfil_view', name='usuarios_perfil_url'),
    
    url(r'^admin/', include(admin.site.urls)),
)
