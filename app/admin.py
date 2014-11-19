from django.contrib import admin
from .models import tag, pregunta, respuesta, comentario, medalla

admin.site.register(tag)
admin.site.register(pregunta)
admin.site.register(respuesta)
admin.site.register(comentario)
admin.site.register(medalla)