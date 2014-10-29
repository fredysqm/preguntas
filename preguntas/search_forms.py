from django import forms
from haystack.forms import SearchForm

class PreguntasSearchForm(SearchForm):
    text = forms.CharField(required=False)
    
    def search(self):
        import pdb; pdb.set_trace()
        sqs = super(PreguntasSearchForm, self).search()        
        
        if not self.is_valid():
            return self.no_query_found()
            
        if self.cleaned_data['text']:
            sqs = sqs.filter(titulo__contains=self.cleaned_data['text'])
            
        return sqs