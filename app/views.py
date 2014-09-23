from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.context_processors import csrf

from .forms import pregunta_form, respuesta_form, tag_form, user_form, pregunta_eliminar_form, respuesta_eliminar_form, comentario_form, comentario_eliminar_form
from .models import pregunta, respuesta, tag, usuario_detalles, usuario_extra, comentario
from django.contrib.auth.models import User


#PREGUNTAS
def preguntas_view(request):
    args = {}
    args['preguntas'] = pregunta.objects.all()
    return render(request, 'preguntas/home.html', args)

def preguntas_crear_view(request):
    args = {}
    if request.POST:
        form = pregunta_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = pregunta_form()
        all_tags = tag.objects.all()

    args.update(csrf(request))
    args['form'] = form
    all_tags = all_tags or []
    args['all_tags'] = all_tags
    return render(request,'preguntas/crear.html', args)

def preguntas_editar_view(request, pregunta_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)
    
    if request.POST:
        form = pregunta_form(request.POST, instance=_pregunta)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = pregunta_form(initial={'titulo':_pregunta.titulo, 'contenido':_pregunta.contenido,
                                      'tags':_pregunta.tags, 'autor':_pregunta.autor})
        all_tags = tag.objects.all()

    args.update(csrf(request))
    args['pregunta'] = _pregunta
    args['form'] = form
    args['all_tags'] = all_tags
    return render(request, 'preguntas/editar.html', args)

def preguntas_eliminar_view(request, pregunta_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)

    if request.POST:
        form = pregunta_eliminar_form(request.POST, instance=_pregunta)

        if form.is_valid():
            _pregunta.delete()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = pregunta_eliminar_form(instance=_pregunta)

    args.update(csrf(request))
    args['form'] = form
    args['pregunta'] = _pregunta
    return render(request, 'preguntas/eliminar.html', args)

def preguntas_responder_view(request,pregunta_id):
    args = {}
    if request.POST:
        form = respuesta_form(request.POST)
        if form.is_valid():
            pregunta_obj = pregunta.objects.filter(id=pregunta_id).values('n_respuestas')[0]
            if pregunta_obj['n_respuestas'] > -1:
                pregunta.objects.filter(id=pregunta_id).update(n_respuestas=(pregunta_obj['n_respuestas']+1),
                                                               respondido=True)
            else:
                pregunta.objects.filter(id=pregunta_id).update(n_respuestas=(pregunta_obj['n_respuestas']+1))
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = respuesta_form(initial={'pregunta':pregunta_id})

    pregunta_obj = get_object_or_404(pregunta, id=pregunta_id)
    pregunta.objects.filter(id=pregunta_id).update(n_vistas=(pregunta_obj.n_vistas + 1))

    respuestas = respuesta.objects.filter(pregunta=pregunta_id)

    args.update(csrf(request))
    args['form'] = form
    args['pregunta'] = pregunta.objects.get(id=pregunta_id)
    args['respuestas'] = respuestas
    return render(request,'preguntas/responder.html', args)

def preguntas_abiertas_view(request):
    args = {}
    preguntas_abiertas = pregunta.objects.filter(n_respuestas=0)
    args['preguntas'] = preguntas_abiertas
    return render(request,'preguntas/home.html',args)

def preguntas_por_tag_view(request, tag_id):
    args = {}
    tagged_preguntas = get_list_or_404(pregunta, tags=tag_id)
    chosen_tag = tag.objects.get(id=tag_id)
    args.update(csrf(request))
    args['tagged'] = tagged_preguntas
    args['tag'] = chosen_tag
    return render(request,'preguntas/tag.html', args)

def preguntas_comentarios_view(request, pregunta_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)
    _comentarios = get_list_or_404(comentario, content_type=11, object_id=pregunta_id)
    args.update(csrf(request))
    args['pregunta'] = _pregunta
    args['comentarios'] = _comentarios
    return render(request,'preguntas/comentarios.html', args)

# RESPUESTAS
def respuestas_editar_view(request, respuesta_id):
    args = {}
    if request.POST:
        _respuesta = respuesta.objects.get(id=respuesta_id)
        form = respuesta_form(request.POST, instance=_respuesta)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        _respuesta = respuesta.objects.get(id=respuesta_id)
        form = respuesta_form(initial={'pregunta':_respuesta.pregunta,
                           'autor':_respuesta.autor, 'contenido':_respuesta.contenido})

    args.update(csrf(request))
    args['respuesta'] = _respuesta
    args['form'] = form
    return render(request, 'respuestas/editar.html', args)

def respuestas_eliminar_view(request, respuesta_id):
    args = {}
    _respuesta = get_object_or_404(respuesta, id=respuesta_id)

    if request.POST:
        form = respuesta_eliminar_form(request.POST, instance=_respuesta)
        if form.is_valid():
            _respuesta.delete()
            pregunta_obj = pregunta.objects.filter(id=_respuesta.pregunta.id).values('n_respuestas')[0]
            if pregunta_obj['n_respuestas'] == 1:
                pregunta.objects.filter(id=_respuesta.pregunta.id).update(n_respuestas=(pregunta_obj['n_respuestas']-1),
                                                               respondido=False)
            else:
                pregunta.objects.filter(id=_respuesta.pregunta.id).update(n_respuestas=(pregunta_obj['n_respuestas']-1))
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = respuesta_eliminar_form(instance=_respuesta)

    args.update(csrf(request))
    args['form'] = form
    args['respuesta'] = _respuesta
    return render(request, 'respuestas/eliminar.html', args)


# TAGS
def tags_crear_view(request):
    args = {}
    if request.POST:
        form = tag_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = tag_form()

    args.update(csrf(request))
    args['form'] = form
    return render(request,'tag_crear.html', args)


def usuarios_perfil_view(request, user_id):
    args = {}
    requested_user = get_object_or_404(User, id=user_id)
    requested_user_details = get_object_or_404(usuario_detalles, usuario_detalles=user_id)
    requested_user_extra = get_object_or_404(usuario_extra, usuario_extra=user_id)
    args['usuario'] = requested_user
    args['usuario_detalles'] = requested_user_details
    args['usuario_extra'] = requested_user_extra
    return render(request, 'usuario/usuarios_perfil.html', args)

# COMENTARIOS
def comentarios_crear_view(request):
    args = {}
    if request.POST:
        form = comentario_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = comentario_form(initial={'n_votos' : 0, 'estado' : 0})
     
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'comentarios/crear.html', args)

def comentarios_editar_view(request, comentario_id):
    args = {}
    _comentario = get_object_or_404(comentario, id=comentario_id)
    if request.POST:        
        form = comentario_form(request.POST, instance=_comentario)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = comentario_form(initial={'content_type':_comentario.content_type,
                           'object_id':_comentario.object_id, 'autor':_comentario.autor, 
                           'contenido':_comentario.contenido, 'n_votos':_comentario.n_votos,
                           'estado':_comentario.estado})

    args.update(csrf(request))
    args['comentario'] = _comentario
    args['form'] = form
    return render(request, 'comentarios/editar.html', args)    

def comentarios_eliminar_view(request, comentario_id):
    # ESTAS AQUI. Tienes que ver que elimine bien el comentario.
    args = {}
    _comentario = get_object_or_404(comentario, id=comentario_id)

    if request.POST:
        form = comentario_eliminar_form(request.POST, instance=_comentario)
        if form.is_valid():
            _comentario.delete()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = comentario_eliminar_form(instance=_comentario)

    args.update(csrf(request))
    args['form'] = form
    args['comentario'] = _comentario
    return render(request, 'comentarios/eliminar.html', args)    
    
# def crear_usuario( request ):
#     args = {}
#     args.update(csrf(request))
#     if request.POST:
#         form = user_form( request.POST )
#         validar_formulario( form )
#         return HttpResponseRedirect( '/' )
#     else:
#         form = user_form()

#     args[ 'form' ] = form
#     return render(request, 'crear_usuario.html', args)

# def crear_respuesta( request ):
#     if request.POST:
#         form = RespuestaForm( request.POST )
#         validar_formulario( form )
#         return HttpResponseRedirect( '/' )
#     else:
#         form = RespuestaForm()

#     args = {}

#     return render_to_response( 'crear_respuesta.html',
#                                preparar_args( args, request, form ) )

# def crear_tag( request ):
#     if request.POST:
#         form = TagForm( request.POST )
#         validar_formulario( form )
#         return HttpResponseRedirect( '/' )
#     else:
#         form = TagForm()

#     args = {}

#     return render_to_response( 'crear_tag.html', preparar_args( args, request ) )


# def respuesta_creada( request ):
#     return render_to_response( 'respuesta_creada.html',
#                                context_instance=RequestContext(request) )
