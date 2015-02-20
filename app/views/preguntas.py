from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from ..forms.preguntas import pregunta_crear_form, pregunta_editar_form
from ..models import pregunta


class preguntas_ultimas_view(ListView):
    queryset = pregunta.objects.all().select_related('tags')
    template_name = 'preguntas/ultimas.html'


class preguntas_crear_view(CreateView):
    form_class = pregunta_crear_form
    success_url = reverse_lazy('preguntas_url')
    template_name = 'preguntas/crear.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(preguntas_crear_view, self).form_valid(form)


class preguntas_editar_view(UpdateView):
    model=pregunta
    form_class = pregunta_editar_form
    success_url = reverse_lazy('preguntas_url')
    template_name = 'preguntas/editar.html'