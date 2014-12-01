from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import usuario_extra, pregunta, usuario_reporte
import uuid

MAXIMO_REPORTES = 10
RANGO_REPORTES = 3

@receiver(post_save, sender=User, dispatch_uid=str(uuid.uuid4()))
def user_post_save(sender=User, **kwargs):
    new_id = kwargs['instance'].pk
    extra = usuario_extra(usuario_extra_id=new_id, rol='U', puntaje=0, descripcion='')
    extra.save()
"""   
@receiver(post_save, sender=pregunta, dispatch_uid=str(uuid.uuid4()))
def pregunta_post_save(sender=pregunta, **kwargs):
    import pdb; pdb.set_trace()
    new_id = kwargs['instance'].pk
    tags = kwargs['instance'].tags
    for this_tag in tags:
        _tag = tag.get(id=this_tag)
        _n_preguntas = _tag.n_preguntas
        _tag.update(n_preguntas=(_n_preguntas+1))
"""

@receiver(post_save, sender=usuario_reporte)
def bloquear_usuario(sender=usuario_reporte, **kwargs):
    if kwargs.get('instance', False):
        _reporte = kwargs.get('instance')
        _reportado = User.objects.get(id=_reporte.reportado.id)
        _reportes = usuario_reporte.objects.filter(reportado=_reporte.reportado.id)[:MAXIMO_REPORTES]
        if _reportes.count() > 9:
            fecha_1 = _reportes[0].fecha_hora
            fecha_2 = _reportes[9].fecha_hora
            if (fecha_2 - fecha_1).days <= RANGO_REPORTES:
                bloqueados = Group.objects.get(name='Bloqueados') 
                grupo = User.groups.through.objects.get(user=_reportado)
                grupo.group = bloqueados
                grupo.save()
