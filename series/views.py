"""Views for series app."""
from django.urls import reverse
from django.views.generic import FormView, View
from series.forms import SearchSeriesForm
from series.APILibrary import search_show, get_show_details
from django.shortcuts import render


# Create your views here.


class SearchSeriesView(FormView):
    """Search for series."""
    template_name = 'series/search_series.html'
    form_class = SearchSeriesForm
    success_url = '/search'

    def get_success_url(self) -> str:
        return reverse(
            'search_results',
            kwargs={'term': self.request.POST['search_term']}
        )


class SearchResultsView(View):
    """Result page after a search by user"""
    template = 'series/search_results.html'

    def get(self, request, term: str):
        shows = search_show(term)
        return render(
            template_name='series/search_results.html',
            request=request,
            context={'shows_list': shows}
        )


class ShowDetailsView(View):
    """Details of a show"""
    template = 'series/show_details.html'

    def get(self, request, id: int):
        show = get_show_details(id)
        return render(
            template_name='series/show_details.html',
            request=request,
            context={'show': show, 'directors': ", ".join(show.directors), 'genres': ", ".join(show.genres)}
        )
