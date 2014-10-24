import datetime
from haystack import indexes
from models import pregunta

class pregunta_index(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    fecha = indexes.DateTimeField(model_attr='fecha_hora')
    
    content_auto = indexes.EdgeNgramField(model_attr='titulo')
    
    def get_model(self):
        return pregunta
        
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    