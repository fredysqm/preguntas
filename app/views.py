from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random

from .forms import pregunta_form, respuesta_form, tag_form, user_form, user_editar_form, user_extra_form, pregunta_eliminar_form, respuesta_eliminar_form, comentario_form, comentario_eliminar_form, usuario_reporte_form, reporte_pregunta_form
from .models import pregunta, contenido, tag, usuario_extra, comentario, voto, favorito, usuario_reporte, contenido_reporte, mejor_respuesta

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

class preguntas_editar_view(UpdateView):
    model = pregunta
    form_class = pregunta_form
    template_name = 'preguntas/editar.html'
    fields = ['texto']
    success_url = '/'    
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        pk = self.kwargs['pk']
        _pregunta = pregunta.objects.get(id=pk)
        if self.request.user.id == _pregunta.id:
            return super(preguntas_editar_view, self).dispatch(*args, **kwargs)
        else:
            raise Http404        
    
    def get_context_data(self, **kwargs):        
        pregunta_id = self.kwargs['pk']
        context = super(preguntas_editar_view, self).get_context_data(**kwargs)
        context['all_tags'] = tag.objects.all()
        context['pregunta'] = self.object
        context['contenido'] = contenido.objects.filter(pregunta=self.object.id)[0]
        return context
        
    def get_initial(self, *args, **kwargs):
        _contenido = contenido.objects.filter(pregunta=self.object.id)[0]        
        _pregunta = self.object
        return {'titulo':_pregunta.titulo, 'contenido':_contenido.texto, 'tags':_pregunta.tags, 'autor':_contenido.autor}
        
    def post(self, *args, **kwargs):
        _pregunta = pregunta.objects.get(id=self.kwargs['pk'])
        _contenido = contenido.objects.filter(pregunta=self.kwargs['pk'])[0]
        contenido.objects.filter(id=_contenido.id).update(texto=self.request.POST['contenido'])
        old_tags = _pregunta.tags.all()
        new_tags = tag.objects.filter(id__in = self.request.POST['tags'])
        to_add = old_tags.exclude(id__in = new_tags)
        _pregunta.tags = to_add
        return super(preguntas_editar_view, self).post(*args, **kwargs)

class preguntas_ver_view(DetailView):
    model = pregunta
    template_name = 'preguntas/ver.html'
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_ver_view, self).get_context_data(**kwargs)
        _pregunta = self.object
        _pregunta_contenido = contenido.objects.filter(pregunta=_pregunta.pk)
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
        context['pregunta_contenido'] = _pregunta_contenido
        context['autor'] = _pregunta.contenido_set.first().autor
        context['respuestas'] = zip(_respuestas, comentarios_respuestas)
        context['comentarios'] = _comentarios
        context['path'] = self.request.path
        context['pregunta_contenido'] = pregunta_contenido
        context['voto'] = _voto.first()
        context['es_favorito'] = True if favorito.objects.filter(pregunta=_pregunta.id) else False
        return context

class preguntas_eliminar_view(DeleteView):
    form_class = pregunta_eliminar_form
    model = pregunta
    success_url = reverse_lazy('preguntas_url')
    template_name = 'preguntas/eliminar.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        pk = self.kwargs['pk']
        _pregunta = pregunta.objects.get(id=pk)
        if self.request.user.id == _pregunta.id:
            return super(preguntas_eliminar_view, self).dispatch(*args, **kwargs)
        else:
            raise Http404 
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_eliminar_view, self).get_context_data(**kwargs)
        context['form'] = pregunta_eliminar_form()
        return context

class preguntas_responder_view(FormView):
    model = contenido
    template_name = 'preguntas/responder.html'
    form_class = respuesta_form
    fields = ['texto']
    success_url = '/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_responder_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(preguntas_responder_view, self).get_context_data(**kwargs)
        contenidos = contenido.objects.filter(pregunta=self.kwargs['pk'])
        context['pregunta'] = pregunta.objects.get(pk=self.kwargs['pk'])
        context['pregunta_contenido'] = contenidos[0]        
        if len(contenidos) > 1:
            context['respuestas'] = contenidos[1:]
        else:
            context['respuestas'] = []
        return context
    
    def post(self, *args, **kwargs):
        context = super(preguntas_responder_view, self).get_context_data(**kwargs)        
        _pregunta = pregunta.objects.get(pk=self.kwargs['pk'])
        context['pregunta'] = _pregunta
        contenidos = contenido.objects.filter(pregunta=self.kwargs['pk'])
        context['pregunta_contenido'] = contenidos[0]
        context['autor'] = User.objects.get(pk=self.request.user.id)
        if len(contenidos) > 1:
            context['respuestas'] = contenidos[1:]
        else:
            context['respuestas'] = []
        _pregunta.n_respuestas = _pregunta.n_respuestas + 1
        _pregunta.save()
        x = super(preguntas_responder_view, self).post(*args, **kwargs)
        _contenido = contenido.objects.create(pregunta=context['pregunta'], autor=context['autor'], texto=self.request.POST['texto'])
        return x

class preguntas_abiertas_view(ListView):
    queryset = pregunta.objects.filter(n_respuestas=0)
    template_name = 'preguntas/home.html'
    object_list = queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super(preguntas_abiertas_view, self).get_context_data(**kwargs)
        context['preguntas'] = self.object_list
        return context

class preguntas_por_tag_view(ListView):
    model = pregunta
    template_name = 'preguntas/tag.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(preguntas_por_tag_view, self).get_context_data(*args, **kwargs)
        tag_id = self.kwargs['tag_id']
        chosen_tag = tag.objects.get(id=tag_id)
        queryset = pregunta.objects.filter(tags = chosen_tag.id)
        object_list = queryset
        context['tagged'] = object_list
        context['tag'] = chosen_tag
        return context
     
class preguntas_favorito_view(DetailView):
    model = pregunta
    template_name = 'preguntas/ver.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(preguntas_favorito_view, self).get_context_data(*args, **kwargs)
        pregunta = self.kwargs['pk']
        favorito.objects.create(user=self.request.user, pregunta=self.object)
        context['autor'] = self.request.user
        return context
        
    def get_success_url(self, *args, **kwargs):
        self.success_url = reverse_lazy('ver', kwargs={'pregunta':self.kwargs['pk']})
        return self.success_url

class preguntas_votar_arriba_view(DetailView):
    model = pregunta
    template_name = 'preguntas/ver.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_votar_arriba_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(preguntas_votar_arriba_view, self).get_context_data(*args, **kwargs)
        pregunta_id = self.kwargs['pk']
        _pregunta = pregunta.objects.get(id=pregunta_id)
        if voto.objects.filter(user=self.request.user, pregunta=_pregunta, valor=1).count() == 0:
            voto.objects.create(user=self.request.user, pregunta=_pregunta, valor=1)
            pregunta.objects.filter(id=_pregunta.id).update(n_votos=(_pregunta.n_votos+1))
        context['autor'] = User.objects.get(id=contenido.objects.filter(pregunta=self.object.id)[0].autor.id)
        return context
        
    def get_success_url(self, *args, **kwargs):        
        return reverse_lazy('ver', kwargs={'pregunta':self.kwargs['pk']})

class preguntas_votar_abajo_view(DetailView):
    model = pregunta
    template_name = 'preguntas/ver.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_votar_abajo_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(preguntas_votar_abajo_view, self).get_context_data(*args, **kwargs)
        pregunta_id = self.kwargs['pk']
        _pregunta = pregunta.objects.get(id=pregunta_id)
        if voto.objects.filter(user=self.request.user, pregunta=_pregunta, valor=-1).count() == 0:
            voto.objects.create(user=self.request.user, pregunta=_pregunta, valor=-1)
            pregunta.objects.filter(id=_pregunta.id).update(n_votos=(_pregunta.n_votos-1))
        context['autor'] = User.objects.get(id=contenido.objects.filter(pregunta=self.object.id)[0].autor.id)
        return context

    def get_success_url(self, *args, **kwargs):
        self.success_url = reverse_lazy('ver', kwargs={'pregunta':self.kwargs['pk']})
        self.template_name = 'preguntas/ver.html'
        return self.success_url

class preguntas_reportar_view(CreateView):
    model = contenido_reporte
    template_name = 'preguntas/reportar.html'
    form_class = reporte_pregunta_form
    fields = ['tipo', 'mensaje']
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_reportar_view, self).dispatch(*args, **kwargs)
        
    # Me falta corregir el success_url
    def post(self, *args, **kwargs):        
        x = super(preguntas_reportar_view, self).post(*args, **kwargs)
        _contenido = contenido.objects.filter(pregunta=self.kwargs['pk'])[0]
        _reporte = contenido_reporte.objects.create(user=self.request.user, contenido=_contenido, tipo=self.request.POST['tipo'], mensaje=self.request.POST['mensaje'])        
        return x
        
    def get_success_url(self, *args, **kwargs):
        return '/ver/' + kwargs['pk']
    
# RESPUESTAS
class respuestas_editar_view(UpdateView):
    model = contenido
    form_class = respuesta_form
    template_name = 'respuestas/editar.html'
    fields = ['texto']
    success_url = '/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(usuarios_perfil_editar_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        respuesta_id = self.kwargs['pk']
        context = super(respuestas_editar_view, self).get_context_data(*args, **kwargs)
        _respuesta = contenido.objects.get(id=respuesta_id)
        context['respuesta'] = _respuesta    
        return context

class respuestas_eliminar_view(DeleteView):
    model = contenido
    success_url = '/'    
    form_class = respuesta_eliminar_form
    template_name = 'respuestas/eliminar.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(respuestas_eliminar_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(preguntas_eliminar_view, self).get_context_data(**kwargs)
        context['form'] = respuesta_eliminar_form()
        return context    

#Falta corregir el success url
class respuestas_elegir_mejor_view(DetailView):
    model = contenido
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(preguntas_elegir_mejor_view, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(respuestas_elegir_mejor_view, self).get_context_data(*args, **kwargs)
        respuesta_id = self.kwargs['pk']
        _respuesta = get_object_or_404(contenido, id=respuesta_id)
        _pregunta = pregunta.objects.get(id=_respuesta.pregunta_id)
        _respuestas = contenido.objects.filter(pregunta=_pregunta.id)
        if mejor_respuesta.objects.filter(pregunta=_pregunta.id).count() > 0:            
            mejor_respuesta.objects.filter(pregunta=_pregunta.id)[0].update(respuesta=_respuesta)
        else:
            mejor_respuesta.objects.create(pregunta=_pregunta,respuesta=_respuesta)
        return context
    
    def get_success_url(self, *args, **kwargs):
        self.success_url = reverse_lazy('ver', kwargs={'pregunta':self.kwargs['pk']})
        return self.success_url

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
class usuarios_ver_view(ListView):
    model = User
    template_name = 'usuarios/ver.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(usuarios_ver_view, self).get_context_data(*args, **kwargs)
        limit = User.objects.count() - 1
        if limit < 10:
            index = random.sample(xrange(1, limit + 1), limit)
        else:
            index = random.sample(xrange(1, limit), 10)
        users = list(User.objects.all()[i] for i in index)
        extra = usuario_extra.objects.filter(usuario_extra__in = users)
        context['usuarios'] = zip(users, extra)
        return context    
    
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

class usuarios_perfil_editar_view(UpdateView):
    model = User
    success_url = reverse_lazy('usuarios_ver_url') 
    template_name = 'usuarios/editar_perfil.html'
    form_maestro = None
    form_detalle = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(usuarios_perfil_editar_view, self).dispatch(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        user_id = self.kwargs['pk']
        requested_user = get_object_or_404(User, id=user_id)
        requested_user_extra = usuario_extra.objects.get(usuario_extra=user_id)
        
        self.form_maestro = user_editar_form(self.request.POST, instance=requested_user)
        self.form_detalle = user_extra_form(self.request.POST, instance=requested_user_extra)
        if self.form_maestro.is_valid() and self.form_detalle.is_valid():
            self.form_maestro.save()
            self.form_detalle.save()
        
        self.success_url = reverse_lazy('usuarios_perfil_url', args=[user_id])
        return super(usuarios_perfil_editar_view, self).post(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        user_id = self.kwargs['pk']
        requested_user = get_object_or_404(User, id=user_id)
        requested_user_extra = usuario_extra.objects.get(usuario_extra=user_id)
        
        self.form_maestro = user_editar_form(initial={'first_name' : requested_user.first_name,
                                      'last_name'  : requested_user.last_name,
                                      'email'      : requested_user.email,})        
        self.form_detalle = user_extra_form(initial={'descripcion' : requested_user_extra.descripcion})
        return super(usuarios_perfil_editar_view, self).get(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(usuarios_perfil_editar_view, self).get_context_data(*args, **kwargs)
        context['form_maestro'] = self.form_maestro
        context['form_detalle'] = self.form_detalle
        context['username'] = self.object.username
        return context
    
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
        return super(comentarios_editar_view, self).dispatch(*args, **kwargs)

class comentarios_eliminar_view(DeleteView):
    form_class = comentario_eliminar_form
    model = comentario
    template_name = 'comentarios/eliminar.html'    
    fields = ['texto']
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.success_url = reverse_lazy('preguntas_ver_url', kwargs={'pk':pregunta.objects.get(pk=contenido.objects.get(pk=comentario.objects.get(pk=kwargs['pk']).contenido.id).pregunta.id).id})
        return super(comentarios_eliminar_view, self).dispatch(self.request, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(comentarios_eliminar_view, self).get_context_data(*args, **kwargs)
        context['form'] = comentario_eliminar_form()
        return context

# Busqueda
class buscar_view(ListView):
    model = pregunta
    template_name = 'preguntas/home.html'
    
    def post(self, *args, **kwargs): 
        self.success_url = '/'
        return super(buscar_view, self).get(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):        
        context = super(buscar_view, self).get_context_data(*args, **kwargs)
        busqueda = self.request.POST['txt_search']
        queryset = pregunta.objects.filter(titulo__search=busqueda)
        pregunta_autor = list()
        for _pregunta in queryset:
            pregunta_autor.append(User.objects.get(id=_pregunta.contenido_set.first().autor.id))
        context['preguntas'] = zip(queryset, pregunta_autor)
        return context

# NOTIFICACIONES
class notificaciones_por_usuario_view(ListView):
    model = notification
    template_name = 'notificaciones/home.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(notificaciones_por_usuario_view, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, *args, **kwargs):
        context = super(notificaciones_por_usuario_view, self).get_context_data(*args, **kwargs)
        context['notifications'] = notification.objects.filter(user=self.request.user, viewed=False)
        return context