from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import usuario_detalles, usuario_extra
import uuid

@receiver(post_save, sender=User, dispatch_uid=str(uuid.uuid4()))
def user_post_save(sender=User, **kwargs):
    new_id = kwargs['instance'].pk
    detalles = usuario_detalles(usuario_detalles_id=new_id, descripcion='')
    detalles.save()
    extra = usuario_extra(usuario_extra_id=new_id, rol='U', puntaje=0)
    extra.save()