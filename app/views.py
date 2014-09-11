from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import PreguntaForm, RespuestaForm, TagForm, UserForm
from models import Pregunta
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

# Variables 

# Metodos auxiliares
def validar_formulario( form ):
    if form.is_valid():
        form.save()

def preparar_args( args, request, form ):
    args.update( csrf( request ) )    
    args[ 'form' ] = form
    return args

# Create your views here.
def index( request ):
    return render_to_response( 'index.html', 
                               context_instance=RequestContext(request) )
# Crear
def crear_usuario( request ):
    if request.POST:
        form = UserForm( request.POST )
        validar_formulario( form )
        return HttpResponseRedirect( '/' )
    else:
        form = UserForm()
     
    args = {}
 
    return render_to_response( 'crear_usuario.html', 
                               preparar_args( args, request, form ) )
    
def crear_pregunta( request ):
    if request.POST:
        form = PreguntaForm( request.POST )
        validar_formulario( form )
        return HttpResponseRedirect( '/' )
    else:
        form = PreguntaForm()
     
    args = {}
 
    return render_to_response( 'crear_pregunta.html', 
                               preparar_args( args, request, form ) )
    
def crear_respuesta( request ):
    if request.POST:
        form = RespuestaForm( request.POST )
        validar_formulario( form )
        return HttpResponseRedirect( '/' )
    else:
        form = RespuestaForm()
     
    args = {}
 
    return render_to_response( 'crear_respuesta.html', 
                               preparar_args( args, request, form ) )
    
def crear_tag( request ):
    if request.POST:
        form = TagForm( request.POST )
        validar_formulario( form )
        return HttpResponseRedirect( '/' )
    else:
        form = TagForm()
     
    args = {}
 
    return render_to_response( 'crear_tag.html', preparar_args( args, request ) )
 
# Listar
def listar_preguntas( request ):
    preguntas = Pregunta.objects.all()
    return render_to_response( 'listar_preguntas.html', 
                               { 'preguntas' : preguntas }, 
                               context_instance=RequestContext(request) )

# Responder
def responder_pregunta( request, pregunta_id ):
    if request.POST:
        # Validar y enviar datos para guardar
        form = RespuestaForm( request.POST )        
        if form.is_valid():
            form.save()
            # Current path (/responder)
            return HttpResponseRedirect( '../exito/respuesta' )
        else:
            print 'El formulario no es valido'
    else:
        # Mostrar formulario vacio para responder
        print 'Voy a responder...'
        form = RespuestaForm( initial = { 'pregunta_id' : pregunta_id, 'autor' : 1,
                                          'n_votos' : 0, 'estado' : 'OP' } )
        pregunta = Pregunta.objects.get( id=pregunta_id )
    
    args = {}
    args = preparar_args( args, request, form )
 
    return render_to_response( 'responder.html', 
                               { 'pregunta' : pregunta, 'form' : form },
                               context_instance=RequestContext(request) )                               

def respuesta_creada( request ):
    return render_to_response( 'respuesta_creada.html', 
                               context_instance=RequestContext(request) )