from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'app.views.preguntas_view', name='preguntas_url'),
    
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/password/reset', 'django.contrib.auth.views.password_reset',
   name='password_reset'),
   
    url(r'^notificationes/', 'app.views.notificaciones_por_usuario_view', name='notificaciones_por_usuario_url'),
    url(r'^notification/', include('notification.urls')),
    
    url(r'^crear/$', 'app.views.preguntas_crear_view', name='preguntas_crear_url'),
    url(r'^ver/(\d+)/$', 'app.views.preguntas_ver_view', name='preguntas_ver_url'),
    url(r'^editar/(\d+)/([\w\-]+)/$', 'app.views.preguntas_editar_view', name='preguntas_editar_url'),
    url(r'^eliminar/(\d+)/$', 'app.views.preguntas_eliminar_view', name='preguntas_eliminar_url'),
    url(r'^responder/(\d+)/$', 'app.views.preguntas_responder_view', name='preguntas_responder_url'),
    url(r'^abiertas/$', 'app.views.preguntas_abiertas_view', name='preguntas_abiertas_url'),
    url(r'^tag/(\d+)/$', 'app.views.preguntas_por_tag_view', name='preguntas_por_tag_url'),
    url(r'^comentarios/(\d+)/$', 'app.views.preguntas_comentarios_view', name='preguntas_comentarios_url'),
    url(r'^favorito/(\d+)/$', 'app.views.preguntas_favorito_view', name='preguntas_favorito_url'),
    url(r'^votar_arriba/(\d+)/$', 'app.views.preguntas_votar_arriba_view', name='preguntas_votar_arriba_url'),
    url(r'^votar_abajo/(\d+)/$', 'app.views.preguntas_votar_abajo_view', name='preguntas_votar_abajo_url'),
    url(r'^reportar/(\d+)/$', 'app.views.preguntas_reportar_view', name='preguntas_reportar_url'),
    
    url(r'^respuestas/(\d+)/editar/$', 'app.views.respuestas_editar_view', name='respuestas_editar_url'),
    url(r'^respuestas/(\d+)/eliminar/$', 'app.views.respuestas_eliminar_view', name='respuestas_eliminar_url'),
    url(r'^respuestas/(\d+)/mejor/$', 'app.views.respuestas_elegir_mejor_view', name='respuestas_elegir_mejor_url'),

    url(r'^tags/ver/$', 'app.views.tags_ver_view', name='tags_ver_url'),
    url(r'^tags/crear/$', 'app.views.tags_crear_view', name='tags_crear_url'),
    url(r'^tags/populares/$', 'app.views.tags_populares_ver_view', name='tags_populares_ver_url'),
    url(r'users/$', 'app.views.usuarios_ver_view', name='usuarios_ver_url'),
    url(r'user/(\d+)/$', 'app.views.usuarios_perfil_view', name='usuarios_perfil_url'),
    url(r'user/(\d+)/editar/$', 'app.views.usuarios_perfil_editar_view', name='usuarios_perfil_editar_url'),

    url(r'^comentarios/crear/$', 'app.views.comentarios_crear_view', name='comentarios_crear_url'),
    url(r'^comentarios/(\d+)/editar/$', 'app.views.comentarios_editar_view', name='comentarios_editar_url'),
    url(r'^comentarios/(\d+)/eliminar/$', 'app.views.comentarios_eliminar_view', name='comentarios_eliminar_url'),
    
    url(r'^usuarios/crear/$', 'app.views.usuario_crear_view', name='usuarios_crear_url'),    
    url(r'^usuarios/(\d+)/perfil/$', 'app.views.usuarios_perfil_view', name='usuarios_perfil_url'),
    url(r'^usuarios/reportar/(\d+)/$', 'app.views.usuarios_reportar_view', name='usuarios_reportar_url'),
    
    url(r'^buscar/$', 'app.views.buscar_view', name='buscar_url'),    
    
)
