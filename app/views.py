from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random

from .forms import pregunta_form, respuesta_form, tag_form, user_form, user_editar_form, user_extra_form, pregunta_eliminar_form, respuesta_eliminar_form, comentario_form, comentario_eliminar_form, usuario_reporte_form, reporte_pregunta_form
from .models import pregunta, contenido, tag, usuario_extra, comentario, voto, favorito, usuario_reporte

from django.utils.decorators import method_decorator

from django.template.defaultfilters import slugify

from notification.models import notification

#PREGUNTAS
class preguntas_lista_view(ListView):          
    queryset = pregunta.objects.all()
    template_name = 'preguntas/home.html'
    object_list = queryset
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_lista_view, self).get_context_data(**kwargs)
        pregunta_autor = list()
        for pregunta in self.object_list:
            pregunta_autor.append(User.objects.get(id=pregunta.contenido_set.first().autor.id))
        context['user'] = self.request.user
        context['preguntas'] = zip(self.object_list, pregunta_autor)
        return context

class preguntas_crear_view(CreateView):
    form_class = pregunta_form
    model = pregunta
    fields = ['titulo', 'tags']
    template_name = 'preguntas/crear2.html'
    success_url = '/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_crear_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_crear_view, self).get_context_data(**kwargs)
        context['contenido'] = ''
        context['all_tags'] = tag.objects.all()
        return context
        
    def post(self, *args, **kwargs):
        x = super(preguntas_crear_view, self).post(*args, **kwargs)
        _contenido = contenido.objects.create(pregunta=self.object, texto=self.request.POST['contenido'], autor=self.request.user)
        return x

@login_required()
def preguntas_editar_view(request, pregunta_id, pregunta_slug):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)
    _contenido = _pregunta.contenido_set.first()

    if _contenido.autor.id == request.user.id:
        if request.POST:
            form = pregunta_form(request.POST, instance=_pregunta)
            if form.is_valid():
                old_tags = _pregunta.tags.all()
                new_tags = form.cleaned_data['tags']
                to_add = old_tags.exclude(id__in = new_tags)
                to_rest = new_tags.exclude(id__in = old_tags)
                for _tag in to_add:
                    _n_preguntas = _tag.n_preguntas
                    tag.objects.filter(id=_tag.id).update(n_preguntas=(_n_preguntas-1))
                for _tag in to_rest:
                    _n_preguntas = _tag.n_preguntas
                    tag.objects.filter(id=_tag.id).update(n_preguntas=(_n_preguntas+1))
                form.save()
                return HttpResponseRedirect(reverse('preguntas_url'))
        else:
            form = pregunta_form(initial={'titulo':_pregunta.titulo, 'contenido':_contenido.texto,
                                        'tags':_pregunta.tags, 'autor':_contenido.autor})
            all_tags = tag.objects.all()

        args.update(csrf(request))
        args['pregunta'] = _pregunta
        args['form'] = form
        args['all_tags'] = all_tags
        return render(request, 'preguntas/editar.html', args)
    else:
        return render(request, 'errores/no_autorizado.html', args)

class preguntas_ver_view(DetailView):
    model = pregunta
    template_name = 'preguntas/ver.html'
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_ver_view, self).get_context_data(**kwargs)
        _pregunta = self.object
        pregunta_id = self.object.id
        user = self.request.user
        respuestas = contenido.objects.filter(pregunta_id=pregunta_id)
        pregunta_contenido = respuestas.first()
        _respuestas = respuestas[1:]
        comentarios_respuestas = []
        for _respuesta in _respuestas.values():
            comentarios_respuestas.append(comentario.objects.filter(contenido=_respuesta['id']))
        _comentarios = comentario.objects.filter(contenido=pregunta_contenido.id)
        _voto = voto.objects.filter(pregunta=_pregunta.id,user=user.id).order_by('-id')[:1]        
        
        pregunta.objects.filter(id=pregunta_id).update(n_vistas=(_pregunta.n_vistas + 1))
        _respuestas = contenido.objects.filter(pregunta_id=pregunta_id)[1:]
        
        context['pregunta'] = _pregunta
        context['autor'] = _pregunta.contenido_set.first().autor
        context['respuestas'] = zip(_respuestas, comentarios_respuestas)
        context['comentarios'] = _comentarios
        context['path'] = self.request.path
        context['pregunta_contenido'] = pregunta_contenido
        context['voto'] = _voto.first()
        return context

class preguntas_eliminar_view(DeleteView):
    form_class = pregunta_eliminar_form
    model = pregunta
    success_url = reverse_lazy('preguntas_url')
    template_name = 'preguntas/eliminar.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_eliminar_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_eliminar_view, self).get_context_data(**kwargs)
        context['contenido'] = ''
        return context
    
@login_required()
def _preguntas_eliminar_view(request, pregunta_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)

    if request.POST:
        form = pregunta_eliminar_form(request.POST, instance=_pregunta)
        if form.is_valid():
            _tags = _pregunta.tags.all()
            for _tag in _tags:
                _n_preguntas = _tag.n_preguntas
                tag.objects.filter(id=_tag.id).update(n_preguntas=(_n_preguntas-1))

            _pregunta.delete()          
                        
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = pregunta_eliminar_form(instance=_pregunta)

    args.update(csrf(request))
    args['form'] = form
    args['pregunta'] = _pregunta
    return render(request, 'preguntas/eliminar.html', args)

class preguntas_responder_view(CreateView):
    model = contenido
    template_name = 'preguntas/responder.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_responder_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_responder_view, self).get_context_data(**kwargs)
        import pdb; pdb.set_trace()
        context['pregunta'] = self.object

"""    
@login_required()
def _preguntas_responder_view(request,pregunta_id):
    args = {}
    if request.POST:
        form = respuesta_form(request.POST)
        if form.is_valid():
            pregunta_obj = pregunta.objects.filter(id=pregunta_id).values('n_respuestas')[0]
            pregunta.objects.filter(id=pregunta_id).update(n_respuestas=(pregunta_obj['n_respuestas']+1))
            form.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = respuesta_form(initial={'pregunta':pregunta_id, 'autor':request.user.id})

    pregunta_obj = get_object_or_404(pregunta, id=pregunta_id)
    pregunta.objects.filter(id=pregunta_id).update(n_vistas=(pregunta_obj.n_vistas + 1))

    respuestas = respuesta.objects.filter(pregunta=pregunta_id)

    args.update(csrf(request))
    args['form'] = form
    args['pregunta'] = pregunta.objects.get(id=pregunta_id)
    args['respuestas'] = respuestas
    return render(request,'preguntas/responder.html', args)
"""
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

def preguntas_favorito_view(request, pregunta_id):
    args = {}    
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)
    _favorito = favorito.objects.get(pregunta=_pregunta.id, user=request.user.id)
    if _favorito:
        favorito.objects.filter(id=_favorito.id).update(estado=1)
    else:
        favorito.objects.create(pregunta=_pregunta.id, user=request.user.id)
    
def preguntas_votar_arriba_view(request, pregunta_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)    
    voto.objects.create(user=request.user, pregunta=_pregunta, arriba=True)
    pregunta.objects.filter(id=_pregunta.id).update(n_votos=(_pregunta.n_votos+1))    
    return HttpResponseRedirect(reverse('preguntas_ver_url', args=[pregunta_id]))

def preguntas_votar_abajo_view(request, pregunta_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=pregunta_id)
    voto.objects.create(user=request.user, pregunta=_pregunta)
    pregunta.objects.filter(id=_pregunta.id).update(n_votos=(_pregunta.n_votos-1))
    return HttpResponseRedirect(reverse('preguntas_ver_url', args=[pregunta_id]))

def preguntas_reportar_view(request, reportada_id):
    args = {}
    _pregunta = get_object_or_404(pregunta, id=reportada_id)
    if request.POST:        
        form = reporte_pregunta_form(request.POST)
        if form.is_valid():            
            _reporte = form.save(commit=False)
            _reporte.user = request.user
            _reporte.pregunta = _pregunta
            _reporte.save()
            return HttpResponseRedirect(reverse('preguntas_url'))
    else:
        form = reporte_usuario_form(initial={'user':request.user,'pregunta':_pregunta,})

    args.update(csrf(request))
    args['form'] = form
    return render(request,'preguntas/reportar.html', args)
    
    #def preguntas_similares_view(request, pregunta_id):
#    args = {}
#    _pregunta = get_object_or_404(pregunta, id=pregunta_id)
#    palabras = _pregunta.slug.split(str='-')
#    palabras = palabras - ['de', 'para', 'el', 'la', 'y']
#    return None
    
# RESPUESTAS
@login_required()
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

@login_required()
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

def respuestas_elegir_mejor_view(request, respuesta_id):
    _respuesta = get_object_or_404(respuesta, id=respuesta_id)
    _pregunta = pregunta.objects.get(id=_respuesta.pregunta_id)
    _respuestas = respuesta.objects.filter(pregunta=_pregunta.id)
    for res in _respuestas:
        if str(res.id) == str(_respuesta.id):
            respuesta.objects.filter(id=respuesta_id).update(mejor=True)
        elif res.mejor:
            respuesta.objects.filter(id=res.id).update(mejor=False)
    return HttpResponseRedirect(reverse('preguntas_ver_url', args=[_respuesta.pregunta_id]))

# TAGS
class tags_ver_view(ListView):
    queryset = tag.objects.all()
    template_name = 'tag/ver.html'
    object_list = queryset

class tags_populares_ver_view(ListView):
    queryset = tag.objects.all().order_by('-nombre')[:20]
    template_name = 'tag/ver.html'
    object_list = queryset

class tags_crear_view(CreateView):
    model = tag
    template_name = 'tag/tag_crear.html'
    form_class = tag_form
    fields = ['nombre']
    success_url = reverse_lazy('tags_ver_url')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(tags_crear_view, self).dispatch(*args, **kwargs)

# USUARIOS
def usuarios_ver_view(request):
    args = {}
    
    limit = User.objects.count() - 1
    if limit < 10:
        index = random.sample(xrange(1, limit + 1), limit)
    else:
        index = random.sample(xrange(1, limit), 10)
    users = list(User.objects.all()[i] for i in index)
    detalle = usuario_detalles.objects.filter(usuario_detalles__in = users)
    extra = usuario_extra.objects.filter(usuario_extra__in = users)
    args.update(csrf(request))        
    args['usuarios'] = zip(users, detalle, extra)
    return render(request, 'usuarios/ver.html', args)
    
class usuarios_perfil_view(DetailView):
    model = User
    template_name = 'usuarios/usuarios_perfil.html'
            
    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs['pk']
        queryset = User.objects.filter(pk=pk)
        return queryset
        
    def get_context_data(self, *args, **kwargs):
        context = super(usuarios_perfil_view, self).get_context_data(*args, **kwargs)
        pk = self.kwargs['pk']
        context['usuario'] = User.objects.get(pk=pk)        
        context['usuario_extra'] = usuario_extra.objects.get(usuario_extra=pk)        
        contenidos = contenido.objects.filter(autor=pk)
        context['preguntas'] = pregunta.objects.filter(id__in = contenidos.values_list('pregunta', flat=True))
        return context
"""
def _usuarios_perfil_view(request, user_id):
    args = {}
    
    requested_user = get_object_or_404(User, id=user_id)
    requested_user_details = usuario_detalles.objects.get(usuario_detalles=user_id)
    requested_user_extra = usuario_extra.objects.get(usuario_extra=user_id)
    
    _preguntas = pregunta.objects.filter(autor=user_id).order_by("-fecha_hora")[:5]
    _respuestas = respuesta.objects.filter(autor=user_id).order_by("-fecha_hora")[:5]
    
    _votos = voto.objects.filter(user=user_id)
    
    args.update(csrf(request))
    args['usuario'] = requested_user
    args['usuario_detalles'] = requested_user_details
    args['usuario_extra'] = requested_user_extra
    args['preguntas'] = _preguntas
    args['respuestas'] = _respuestas
    args['votos_total'] = _votos.count()
    args['votos_arriba'] = _votos.filter(arriba=True).count()
    args['votos_abajo'] = _votos.filter(arriba=False).count()
    return render(request, 'usuarios/usuarios_perfil.html', args)
"""
@login_required()
def usuarios_perfil_editar_view(request, user_id):
    args = {}
    requested_user = get_object_or_404(User, id=user_id)
    requested_user_details = usuario_detalles.objects.get(usuario_detalles=user_id)
    requested_user_extra = usuario_extra.objects.get(usuario_extra=user_id)
    
    if request.POST:
        form_maestro = user_editar_form(request.POST, instance=requested_user)
        form_detalle = user_detalles_form(request.POST, instance=requested_user_details)
        if form_maestro.is_valid() and form_detalle.is_valid():
            form_maestro.save()
            form_detalle.save()
            return HttpResponseRedirect(reverse('usuarios_perfil_url', args=[user_id]))
    else:
        form_maestro = user_editar_form(initial={'first_name' : requested_user.first_name,
                                      'last_name'  : requested_user.last_name,
                                      'email'      : requested_user.email,})        
        form_detalle = user_detalles_form(initial={'descripcion' : requested_user_details.descripcion})
            
    args.update(csrf(request))
    args['form_maestro'] = form_maestro
    args['form_detalle'] = form_detalle
    return render(request, 'usuarios/editar_perfil.html', args)
    
class usuarios_reportar_view(CreateView):
    model = usuario_reporte
    template_name = 'usuarios/reportar.html'
    form_class = usuario_reporte_form
    success_url = '/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(usuarios_reportar_view, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.reportado = User.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        return super(usuarios_reportar_view, self).form_valid(form)
    
    def post(self, *args, **kwargs):
        return super(usuarios_reportar_view, self).post(self.request, **kwargs)
   
# COMENTARIOS
class comentarios_crear_view(CreateView):
    model = comentario
    template_name = 'comentarios/crear.html'
    form_class = comentario_form
    success_url = '/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(comentarios_crear_view, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        pregunta_contenido = self.request.GET['object_id']
        self.object.contenido = contenido.objects.get(pk=pregunta_contenido)
        self.object.autor = self.request.user
        self.object.save()
        return super(comentarios_crear_view, self).form_valid(form)

class comentarios_editar_view(UpdateView):
    model = comentario
    template_name = 'comentarios/editar.html'
    fields = ['texto']
    form_class = comentario_form  
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.success_url = reverse_lazy('preguntas_ver_url', kwargs={'pk':pregunta.objects.get(pk=contenido.objects.get(pk=comentario.objects.get(pk=kwargs['pk']).contenido.id).pregunta.id).id})
        import pdb; pdb.set_trace()
        return super(comentarios_editar_view, self).dispatch(*args, **kwargs)

class comentarios_eliminar_view(DeleteView):
    form_class = comentario_eliminar_form
    model = comentario
    template_name = 'comentarios/eliminar.html'    
    fields = ['texto']
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.success_url = reverse_lazy('preguntas_ver_url', kwargs={'pk':pregunta.objects.get(pk=contenido.objects.get(pk=comentario.objects.get(pk=kwargs['pk']).contenido.id).pregunta.id).id})
        import pdb; pdb.set_trace()
        return super(comentarios_eliminar_view, self).dispatch(self.request, **kwargs)
    
@login_required()
def _comentarios_eliminar_view(request, comentario_id):
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

@login_required()
def usuario_crear_view( request ):
    args = {}
    args.update(csrf(request))
    if request.POST:
        form = user_form( request.POST )
        if form.is_valid():
            return HttpResponseRedirect( '/' )
    else:
        form = user_form()

    args[ 'form' ] = form
    return render(request, 'usuarios/crear_usuario.html', args)

# Busqueda
class buscar_view(ListView):
    model = pregunta
    template_name = 'preguntas/home.html'
    
    def get(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        return super(buscar_view, self).get(*args, **kwargs)
        
    def post(self, *args, **kwargs): 
        import pdb; pdb.set_trace()
        return super(buscar_view, self).get(*args, **kwargs)
    
    def get_kwargs(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        busqueda = self.request.POST['txt_search']
        queryset = pregunta.objects.filter(titulo__search=busqueda)
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        busqueda = self.request.POST['txt_search']
        queryset = pregunta.objects.filter(titulo__search=busqueda)
        return queryset

def _buscar_view(request):
    args = {}
    busqueda = request.POST['txt_search']
    _preguntas = pregunta.objects.filter(titulo__search=busqueda)
    args['preguntas'] = _preguntas
    #return render(request, 'busqueda/busqueda_preguntas.html', args)
    return render(request, 'preguntas/home.html', args)

# NOTIFICACIONES
class notificaciones_por_usuario_view(ListView):
    model = notification
    template_name = 'notificaciones/home.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(notificaciones_por_usuario_view, self).dispatch(*args, **kwargs)

def _notificaciones_por_usuario_view(request):
    args = {}
    n = notification.objects.filter(user=request.user, viewed=False)
    args['notifications'] = n
    return render(request, 'notificaciones/home.html', args)