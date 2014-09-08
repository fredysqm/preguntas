from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import PreguntaForm, RespuestaForm, TagForm, UserForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

# Create your views here.
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def crear_usuario(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
 
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
     
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
 
    return render_to_response('crear_usuario.html', args)
    
def crear_pregunta(request):
    if request.POST:
        form = PreguntaForm(request.POST)
        if form.is_valid():
            form.save()
 
            return HttpResponseRedirect('/')
    else:
        form = PreguntaForm()
     
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
 
    return render_to_response('crear_pregunta.html', args)
    
def crear_respuesta(request):
    if request.POST:
        form = RespeustaForm(request.POST)
        if form.is_valid():
            form.save()
 
            return HttpResponseRedirect('/')
    else:
        form = RespuestaForm()
     
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
 
    return render_to_response('crear_respuesta.html', args)
    
def crear_tag(request):
    if request.POST:
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
 
            return HttpResponseRedirect('/')
    else:
        form = TagForm()
     
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
 
    return render_to_response('crear_tag.html', args)