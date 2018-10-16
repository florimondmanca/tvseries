"""Views for series app."""
from django.urls import reverse
from django.views.generic import FormView, View
from series.forms import SearchSeriesForm
from series.show import Show
from series.APILibrary import search_show
from django.shortcuts import render
from django.http import HttpResponseRedirect


# Create your views here.


class SearchSeriesView(FormView):
    """Search for series."""
    template_name = 'series/search_series.html'
    form_class = SearchSeriesForm
    success_url = '/search'

    def get_success_url(self):
        return reverse('search_results', kwargs={'term': self.request.POST['search_term']})


class SearchResultsView(View):
    """Result page after a search by user"""
    template = 'series/search_results.html'

    def get(self, request, term: str):
        print("request ={}".format(request))
        shows = search_show(term)
        return render(template_name='series/search_results.html', request=request, context={'shows_list': shows})
