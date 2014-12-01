from django.contrib import admin
from .models import tag, pregunta, contenido, comentario, medalla

admin.site.register(tag)
admin.site.register(pregunta)
admin.site.register(contenido)
admin.site.register(comentario)
admin.site.register(medalla)