from django.conf.urls.defaults import *
from search_forms import PreguntasSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory

sqs = SearchQuerySet().all()


urlpatterns = patterns('',
    url(r'^pregunta/', search_view_factory(
        view_class=SearchView,
        template='search/search_pregunta.html',
        searchqueryset=sqs,
        form_class=PreguntasSearchForm
    ), name='haystack_search_1'),
)