from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf

from .forms import pregunta_form, respuesta_form, tag_form, user_form
from .models import pregunta, tag


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

def preguntas_responder_view(request,pregunta_id):
    args = {}
    if request.POST:
        form = respuesta_form(request.POST)
        if form.is_valid():
            pregunta_obj = pregunta.objects.filter(id=pregunta_id).values('n_respuestas')[0]
            pregunta.objects.filter(id=pregunta_id).update(n_respuestas=(pregunta_obj['n_respuestas']+1))
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = respuesta_form(initial={'pregunta':pregunta_id,})

    args.update(csrf(request))
    args['form'] = form
    args['pregunta'] = pregunta.objects.get(id=pregunta_id)
    return render(request,'preguntas_responder.html', args)

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