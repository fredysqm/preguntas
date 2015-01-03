from django.conf.urls import patterns, url
from views import show_notification

urlpatterns = patterns('',
    #url(r'^notificationes/', 'app.views.notificaciones_por_usuario_view', name='notificaciones_por_usuario_url'),
    url(r'^show/(?P<pk>\d+)/$', show_notification.as_view()),
    url(r'^delete/(?P<notification_id>\d+)/$', 'notification.views.delete_notification')
)