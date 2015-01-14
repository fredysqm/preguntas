# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Button, HTML, Hidden
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, AppendedText, FormActions

from .models import pregunta, contenido, tag, comentario, usuario_extra, usuario_reporte, contenido_reporte

class pregunta_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):     
        
        self.contenido = forms.CharField(required=True)
        
        super(pregunta_form, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'                
        
        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Crear Pregunta',
                'titulo',
                HTML("""<div id="div_id_contenido" class="form-group">
                            <label for="id_contenido" class="control-label col-md-3 requiredField">
                            Contenido<span class="asteriskField">*</span></label>
                            <div class="controls col-md-9">
                                <textarea class="textarea form-control" cols="40" id="id_contenido" name="contenido" rows="10">{{ contenido.texto }}</textarea>
                            </div>
                        </div>"""),
                HTML("""<div id="div_id_tags" class="form-group">
                            <label for="id_tags" class="control-label col-md-3 requiredField">
                            Tags<span class="asteriskField">*</span></label>
                            <div class="controls col-md-9">
                                <select multiple="multiple" class="select form-control" id="id_tags" name="tags">
                                {% for tag in all_tags %}
                                    <option value="{{ tag.id }}" {% if tag in pregunta.tags.all %}selected{% endif %}>{{ tag.nombre }}</option>
                                {% endfor %}
                                </select>
                            </div>
                        </div>"""),
            ),
            FormActions(                
                Submit('submit', u'Guardar'),
                css_class='text-right'
            ),
        )

    class Meta:
        model = pregunta
        exclude = ('n_vistas', 'n_respuestas', 'n_votos', 'respondido', 'estado', 'slug')
    
class pregunta_eliminar_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(pregunta_eliminar_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
        self.helper.layout = Layout(
            Fieldset("""<span class="glyphicon glyphicon-pencil"></span> Quiere eliminar la siguiente 
                        pregunta?
                        <h2><strong>{{ pregunta.titulo }}</strong></h2>
                        <p>{{ pregunta.contenido }}</p>
                        <ul>
                            <li>Por {{ pregunta.autor }}</li>
                            <li>{{ pregunta.n_respuestas }} Respuestas</li>
                            <li>Votos {{ pregunta.n_votos }}</li>
                            <li>{{ pregunta.n_vistas }} Vistas</li>
                        </ul>""",
            ),
            FormActions(                
                Submit('submit', u'Eliminar'),
                css_class='text-right'
            ),
        )
    
    class Meta:
        model = pregunta
        exclude = ('slug', 'titulo', 'contenido', 'pregunta', 'autor', 'n_vistas', 'n_votos', 'n_respuestas', 'estado', 'tags')

class reporte_pregunta_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(reporte_pregunta_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Reportar pregunta',
                Field('tipo'),
                'mensaje',
            ),
            FormActions(
                Submit('submit', u'Reportar'),
                css_class='text-right'
            ),
        )
    
    class Meta:
        model = contenido_reporte
        exclude = ('estado','fecha_hora', 'user', 'pregunta', 'reportado')
        
class user_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email',)

class user_editar_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(user_editar_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
        self.helper.layout = Layout(
            Fieldset("""<span class="glyphicon glyphicon-pencil"></span> Editar perfil - {{ username }}""",
                'first_name',
                'last_name',
                'email',
            ),
        )
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)
        
class user_extra_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(user_extra_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
        self.helper.layout = Layout(
            Fieldset("",
                'descripcion',
            ),
            FormActions(                
                Submit('submit', u'Guardar'),
                css_class='text-right'
            ),
        )    
    
    class Meta:
        model = usuario_extra
        fields = ('descripcion',)
        
class respuesta_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(respuesta_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
        self.helper.layout = Layout(
            Fieldset("""<span class="glyphicon glyphicon-pencil"></span> Respuesta<hr/>
                        """,
                        'texto',
            ),
            FormActions(                
                Submit('submit', u'Guardar'),
                css_class='text-right'
            ),
        )
    
    class Meta:
        model = contenido
        exclude = ('n_votos', 'estado', 'pregunta', 'autor')

class respuesta_eliminar_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(respuesta_eliminar_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
        self.helper.layout = Layout(
            Fieldset("""<span class="glyphicon glyphicon-pencil"></span> Quiere eliminar la siguiente 
                        respuesta?<hr/>
                        <p>{{ respuesta.contenido }}</p>
                        <p><strong>Autor: {{ respuesta.autor }}</strong> -- {{ respuesta.fecha_hora }}</p>
                        <p>Respondida hace...</p>""",
            ),
            FormActions(                
                Submit('submit', u'Eliminar'),
                css_class='text-right'
            ),
        )
    
    class Meta:
        model = contenido
        exclude = ('pregunta', 'autor', 'contenido', 'n_votos', 'estado')

class tag_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(tag_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Crear Tag',
                'nombre',
            ),
            FormActions(
                Submit('submit', u'Crear'),
                css_class='text-right'
            ),
        )
    
    class Meta:
        model = tag
        exclude = ('slug',)

class comentario_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(comentario_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Crear comentario',
                'texto',
            ),
            FormActions(
                Submit('submit', u'Crear'),
                css_class='text-right'
            ),
        )
    
    class Meta:
        model = comentario
        fields = ('texto',)

class comentario_eliminar_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(comentario_eliminar_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
        self.helper.layout = Layout(
            Fieldset("""<span class="glyphicon glyphicon-pencil"></span> Quiere eliminar el siguiente 
                        comentario?<hr/>
                        <h3><strong>{{ comentario.texto }}</strong></h3>
                        <p>{{ comentario.autor }}</p>""",
            ),
            FormActions(                
                Submit('submit', u'Eliminar'),
                css_class='text-right'
            ),
        )
        
    class Meta:
        model = comentario
        exclude = ('content_type', 'object_id', 'autor', 'contenido', 'n_votos', 'estado',)
        
class usuario_reporte_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(usuario_reporte_form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset('<span class="glyphicon glyphicon-pencil"></span> Reportar usuario',
                Field('tipo'),
                'mensaje',
            ),
            FormActions(
                Submit('submit', u'Reportar'),
                css_class='text-right'
            ),
            
        )
    
    class Meta:
        model = usuario_reporte
        fields = ('tipo', 'mensaje')