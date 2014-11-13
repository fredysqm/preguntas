from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    
@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        notification.objects.create(user=kwargs.get('instance'),
                                    title='Welcome to our Django site!',
                                    message='Thanks for signin')