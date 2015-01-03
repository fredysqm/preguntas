from django.views.generic import DetailView

from django.http import HttpResponseRedirect
from models import notification
from django.core.urlresolvers import reverse

# Ejemplos
class show_notification(DetailView):
    model = notification
    template_name = 'notification.html'

    def get_context_data(self, *args, **kwargs):
        context = super(show_notification, self).get_context_data(*args, **kwargs)
        notification_id = self.kwargs['pk']
        queryset = notification.objects.get(id=notification_id)
        context['notification'] = queryset
        return context  
        
def delete_notification(request, notification_id):
    n = notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    return HttpResponseRedirect('/notificationes/')
