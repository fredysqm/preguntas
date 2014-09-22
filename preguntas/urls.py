from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',
    url(r'^$', 'preguntas_view', name='preguntas_url'),
    url(r'^crear/$', 'preguntas_crear_view', name='preguntas_crear_url'),
    url(r'^editar/(\d+)/$', 'preguntas_editar_view', name='preguntas_editar_url'),
    url(r'^eliminar/(\d+)/$', 'preguntas_eliminar_view', name='preguntas_eliminar_url'),
    url(r'^responder/(\d+)/$', 'preguntas_responder_view', name='preguntas_responder_url'),
    url(r'^abiertas/$', 'preguntas_abiertas_view', name='preguntas_abiertas_url'),
    url(r'^tag/(\d+)/$', 'preguntas_por_tag_view', name='preguntas_por_tag_url'),

    url(r'^respuestas/(\d+)/editar/$', 'respuestas_editar_view', name='respuestas_editar_url'),
    url(r'^respuestas/(\d+)/eliminar/$', 'respuestas_eliminar_view', name='respuestas_eliminar_url'),

    url(r'^tags/crear/$', 'tags_crear_view', name='tags_crear_url'),
    url(r'user/(\d+)/$', 'usuarios_perfil_view', name='usuarios_perfil_url'),
    url(r'^admin/', include(admin.site.urls)),
)
