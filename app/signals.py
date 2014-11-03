from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import usuario_detalles, usuario_extra, pregunta
import uuid

@receiver(post_save, sender=User, dispatch_uid=str(uuid.uuid4()))
def user_post_save(sender=User, **kwargs):
    new_id = kwargs['instance'].pk
    detalles = usuario_detalles(usuario_detalles_id=new_id, descripcion='')
    detalles.save()
    extra = usuario_extra(usuario_extra_id=new_id, rol='U', puntaje=0)
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