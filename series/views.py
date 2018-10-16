"""Views for series app."""

import os
from django.views.generic import FormView, CreateView
from series.forms import SearchSeriesForm, SignUpForm
from users.models import User


# Create your views here.


class SearchSeriesView(FormView):
    """Search for series."""
    template_name = 'series/search_series.html'
    form_class = SearchSeriesForm
    success_url = '/'

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = os.path.join('series', 'signup.html')