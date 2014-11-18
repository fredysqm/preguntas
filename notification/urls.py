from django.conf.urls import patterns, url

urlpatterns = patterns('',
    #url(r'^notificationes/', 'app.views.notificaciones_por_usuario_view', name='notificaciones_por_usuario_url'),
    url(r'^show/(?P<notification_id>\d+)/$', 'notification.views.show_notification'),
    url(r'^delete/(?P<notification_id>\d+)/$', 'notification.views.delete_notification')
)