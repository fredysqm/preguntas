from django import template
from notification.models import notification

register = template.Library()

@register.inclusion_tag('notificaciones.html', takes_context=True)
def notificaciones(context):
    _items = notification.objects.filter(user=context.get('user').id, viewed=False)
    return {'number': _items.count()}