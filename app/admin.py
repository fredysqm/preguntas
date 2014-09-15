from django.contrib import admin
from .models import tag, pregunta, respuesta, comentario

admin.site.register(tag)
admin.site.register(pregunta)
admin.site.register(respuesta)
admin.site.register(comentario)