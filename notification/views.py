from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from models import notification
from app.models import respuesta, pregunta
from django.core.urlresolvers import reverse

# Ejemplos
def show_notification(request, notification_id):
    n = notification.objects.get(id=notification_id)
    return render(request, 'notification.html', {'notification' : n})
    

def delete_notification(request, notification_id):
    n = notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()    
    return HttpResponseRedirect('/notificationes/')
