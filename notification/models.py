# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from app.models import respuesta,pregunta, medalla, medalla_usuario

class notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    
@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        notification.objects.create(user=kwargs.get('instance'),
                                    title='Welcome to our Django site!',
                                    message='Thanks for signin')

# Respuesta
@receiver(post_save, sender=respuesta)
def notificacion_respuesta_crear_view(sender, **kwargs):
    if kwargs.get('created', False):
        respuesta = kwargs.get('instance')
        pregunta_autor = pregunta.objects.get(id=respuesta.pregunta_id).autor
        notification.objects.create(user=pregunta_autor,
                                    title='Nueva respuesta',
                                    message='Alguien respondio tu pregunta.')

# Medallas
@receiver(post_save, sender=pregunta)
def notificacion_medalla_curioso_view(sender, **kwargs):
    if kwargs.get('instance', False):
        _pregunta = kwargs.get('instance')
        _n_preguntas = pregunta.objects.filter(autor=_pregunta.autor.id).count()
        _autor = User.objects.get(id=_pregunta.autor.id)
        _otorgado = medalla_usuario.objects.filter(user=_pregunta.autor, medalla=1).exists()
        _medalla = medalla.objects.get(id=1)
        if _n_preguntas == 10 and not _otorgado:
            medalla_usuario.objects.create(user=_pregunta.autor, medalla=_medalla)
            notification.objects.create(user=_autor,
                                        title='Nueva medalla: Curioso',
                                        message='Diez preguntas formuladas. ¡Fantastico!')
                                        
# Usuario bloqueado
@receiver(m2m_changed, sender=User.groups.through)
def notificacion_usuario_bloqueado(sender, **kwargs):
    #A veces no entra
    import pdb; pdb.set_trace()
    if kwargs.get('instance', False) and kwargs.get('action')=='post_add':
        _user = kwargs.get('instance')
        i = 0
        _grupos = _user.groups.all()
        if _grupos.count() > 0:            
            while i < _grupos.count() and _grupos[i].name != 'Bloqueado':                
                i = i + 1
            else:                
                notification.objects.create(user=_user,
                                            title='Esta cuenta ha sido bloqueada',
                                            message='La cuenta ha sido bloqueada. Pongase en contacto con el administrador.')