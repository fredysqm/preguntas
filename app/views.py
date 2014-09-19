from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf

from .forms import pregunta_form, respuesta_form, tag_form, user_form, pregunta_eliminar_form, respuesta_eliminar_form
from .models import pregunta, respuesta, tag, usuario_detalles, usuario_extra
from django.contrib.auth.models import User


#HOME
def home_view(request):
    return render(request, 'home.html')


#PREGUNTAS
def preguntas_view(request):
    args = {}
    args['preguntas'] = pregunta.objects.all()
    return render(request, 'preguntas.html', args)

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
    args['all_tags'] = all_tags
    return render(request,'preguntas_crear.html', args)

def preguntas_editar_view(request, pregunta_id):
    args = {}
    if request.POST:
        _pregunta = pregunta.objects.get(id=pregunta_id)
        form = pregunta_form(request.POST, instance=_pregunta)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        _pregunta = pregunta.objects.get(id=pregunta_id)
        form = pregunta_form(initial={'titulo':_pregunta.titulo, 'contenido':_pregunta.contenido,
                                      'tags':_pregunta.tags, 'autor':_pregunta.autor})
        all_tags = tag.objects.all()
    
    args.update(csrf(request))
    args['pregunta'] = _pregunta
    args['form'] = form
    args['all_tags'] = all_tags    
    return render(request, 'preguntas_editar.html', args)

def preguntas_eliminar_view(request, pregunta_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)
    
    if request.POST:
        form = pregunta_eliminar_form(request.POST, instance=_pregunta)
        
        if form.is_valid():
            _pregunta.delete()
            return HttpResponseRedirect("/")
    else:
        form = pregunta_eliminar_form(instance=_pregunta)

    args.update(csrf(request))
    args['form'] = form
    args['pregunta'] = _pregunta
    return render(request, 'preguntas_eliminar.html', args)
    
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

    pregunta_obj = pregunta.objects.filter(id=pregunta_id).values('n_vistas')[0]
    pregunta.objects.filter(id=pregunta_id).update(n_vistas=(pregunta_obj['n_vistas']+1))
    
    respuestas = respuesta.objects.filter(pregunta=pregunta_id)
    
    args.update(csrf(request))
    args['form'] = form
    args['pregunta'] = pregunta.objects.get(id=pregunta_id)
    args['respuestas'] = respuestas
    return render(request,'preguntas_responder.html', args)

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
    return render(request, 'respuestas_editar.html', args)
    
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
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = respuesta_eliminar_form(instance=_respuesta)

    args.update(csrf(request))
    args['form'] = form
    args['respuesta'] = _respuesta
    return render(request, 'respuestas_eliminar.html', args)
    
# TAGS
def tags_crear_view(request):
    args = {}
    if request.POST:
        form = tag_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home_url'))
    else:
        form = tag_form()

    args.update(csrf(request))
    args['form'] = form
    return render(request,'tag_crear.html', args)
    
def preguntas_tagged_view(request, tag_id):
    args = {}
    tagged_preguntas = pregunta.objects.filter(tags=tag_id)
    chosen_tag = tag.objects.get(id=tag_id)
    args.update(csrf(request))
    args['tagged'] = tagged_preguntas
    args['tag'] = chosen_tag
    return render(request,'preguntas_tagged.html', args)

def preguntas_abiertas_view(request):
    args = {}
    preguntas_abiertas = pregunta.objects.filter(n_respuestas=0)
    args['preguntas'] = preguntas_abiertas
    return render(request,'preguntas.html',args)
    
def usuarios_perfil_view(request, user_id):
    args = {}
    requested_user = User.objects.get(id=user_id)
    requested_user_details = usuario_detalles.objects.get(usuario_detalles=user_id)
    requested_user_extra = usuario_extra.objects.get(usuario_extra=user_id)
    args['usuario'] = requested_user
    args['usuario_detalles'] = requested_user_details
    args['usuario_extra'] = requested_user_extra
    return render(request, 'usuarios_perfil.html', args)
    
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
