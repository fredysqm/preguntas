from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import notification

def show_notification(request, notification_id):
    n = notification.objects.get(id=notification_id)
    return render(request, 'notification.html', {'notification' : n})
    

def delete_notification(request, notification_id):
    n = notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    
    return HttpResponseRedirect('/')