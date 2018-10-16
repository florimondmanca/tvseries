"""Views for series app."""

from django.views.generic import FormView
from series.forms import SearchSeriesForm


# Create your views here.


class SearchSeriesView(FormView):
    """Search for series."""
    template_name = 'series/search_series.html'
    form_class = SearchSeriesForm
    success_url = '/'
