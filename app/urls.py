from django.conf.urls import patterns, include, url
from app.views import preguntas_lista_view, preguntas_crear_view, preguntas_ver_view, preguntas_responder_view, preguntas_eliminar_view, tags_ver_view, tags_populares_ver_view, tags_crear_view, usuarios_perfil_view, usuarios_reportar_view, comentarios_crear_view, buscar_view,notificaciones_por_usuario_view, comentarios_editar_view, comentarios_eliminar_view, preguntas_abiertas_view, preguntas_por_tag_view, preguntas_reportar_view, respuestas_editar_view, usuarios_ver_view, usuarios_perfil_editar_view, respuestas_eliminar_view, preguntas_editar_view, preguntas_favorito_view, preguntas_votar_arriba_view, preguntas_votar_abajo_view, respuestas_elegir_mejor_view

urlpatterns = patterns('',
    url(r'^$', preguntas_lista_view.as_view(), name='preguntas_url'),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/password/reset', 'django.contrib.auth.views.password_reset', name='password_reset'),

    url(r'^notificationes/', notificaciones_por_usuario_view.as_view(), name='notificaciones_por_usuario_url'),
    url(r'^notification/', include('notification.urls')),

    url(r'^crear/$', preguntas_crear_view.as_view(), name='preguntas_crear_url'),
    url(r'^ver/(?P<pk>[\d]+)/$', preguntas_ver_view.as_view(), name='preguntas_ver_url'),
    url(r'^editar/(?P<pk>[\d]+)/(?P<slug>[\w\-]+)/$', preguntas_editar_view.as_view(), name='preguntas_editar_url'),
    url(r'^eliminar/(?P<pk>[\d]+)/$', preguntas_eliminar_view.as_view(), name='preguntas_eliminar_url'),
    url(r'^responder/(?P<pk>(\d+))/$', preguntas_responder_view.as_view(), name='preguntas_responder_url'),
    url(r'^abiertas/$', preguntas_abiertas_view.as_view(), name='preguntas_abiertas_url'),
    url(r'^tag/(?P<tag_id>[\d]+)/$', preguntas_por_tag_view.as_view(), name='preguntas_por_tag_url'),
    url(r'^favorito/(?P<pk>\d+)/$', preguntas_favorito_view.as_view(), name='preguntas_favorito_url'),
    url(r'^votar_arriba/(?P<pk>\d+)/$', preguntas_votar_arriba_view.as_view(), name='preguntas_votar_arriba_url'),
    url(r'^votar_abajo/(?P<pk>\d+)/$', preguntas_votar_abajo_view.as_view(), name='preguntas_votar_abajo_url'),
    url(r'^reportar/(?P<pk>[\d]+)/$', preguntas_reportar_view.as_view(), name='preguntas_reportar_url'),

    url(r'^respuestas/(?P<pk>[\d]+)/editar/$', respuestas_editar_view.as_view(), name='respuestas_editar_url'),
    url(r'^respuestas/(?P<pk>[\d]+)/eliminar/$', respuestas_eliminar_view.as_view(), name='respuestas_eliminar_url'),
    url(r'^respuestas/(?P<pk>\d+)/mejor/$', respuestas_elegir_mejor_view.as_view(), name='respuestas_elegir_mejor_url'),

    url(r'^tags/ver/$', tags_ver_view.as_view(), name='tags_ver_url'),
    url(r'^tags/crear/$', tags_crear_view.as_view(), name='tags_crear_url'),
    url(r'^tags/populares/$', tags_populares_ver_view.as_view(), name='tags_populares_ver_url'),
    url(r'users/$', usuarios_ver_view.as_view(), name='usuarios_ver_url'),
    url(r'user/(?P<pk>[\d]+)/editar/$', usuarios_perfil_editar_view.as_view(), name='usuarios_perfil_editar_url'),

    url(r'^comentarios/crear/', comentarios_crear_view.as_view(), name='comentarios_crear_url'),
    url(r'^comentarios/(?P<pk>[\d]+)/editar/$', comentarios_editar_view.as_view(), name='comentarios_editar_url'),
    url(r'^comentarios/(?P<pk>[\d]+)/eliminar/$', comentarios_eliminar_view.as_view(), name='comentarios_eliminar_url'),

    url(r'^usuarios/(?P<pk>[\d+])/perfil/$', usuarios_perfil_view.as_view(), name='usuarios_perfil_url'),
    url(r'^usuarios/reportar/(?P<pk>\d+)/$', usuarios_reportar_view.as_view(), name='usuarios_reportar_url'),

    url(r'^buscar/$', buscar_view.as_view(), name='buscar_url'),

)
