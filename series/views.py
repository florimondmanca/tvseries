"""Views for series app."""
from django.urls import reverse
from django.views.generic import FormView, View
from series.forms import SearchSeriesForm
from tmdb.shortcuts import search_shows, retrieve_show
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import APIShow


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
        shows = search_shows(term)
        return render(
            template_name='series/search_results.html',
            request=request,
            context={'shows_list': shows, 'search_term': term}
        )


class ShowDetailsView(View):
    """Details of a show"""
    template = 'series/show_details.html'

    def get(self, request, id: int):
        show = retrieve_show(id)
        return render(
            template_name='series/show_details.html',
            request=request,
            context={'show': show}
        )


class FollowedSeriesView(LoginRequiredMixin, ListView):
    """Page to display the followed series of a user."""
    template_name = 'series/followed_series.html'
    context_object_name = 'followed_series_list'

    # login_url = '/accounts/login/'
    redirect_field_name = ''

    def get_queryset(self):
        return APIShow.objects.filter(followers=self.request.user)

    # def get_redirect_url(self):
    #     """Return the user-originating redirect URL if it's safe."""
    #     redirect_to = self.request.POST.get(
    #         self.redirect_field_name,
    #         self.request.GET.get(self.redirect_field_name, '')
    #     )
    #     return redirect_to
