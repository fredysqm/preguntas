from django import forms
from haystack.forms import SearchForm
from app.models import pregunta

class PreguntasSearchForm(SearchForm):    
    def search(self):        
        sqs = super(PreguntasSearchForm, self).search()        
        
        if not self.is_valid():
            return self.no_query_found()
            
        if self.cleaned_data['q']:
            import pdb; pdb.set_trace()
            sqs = sqs.filter(titulo__contains=self.cleaned_data['q']).models(pregunta)
            
        return sqs