"""Views for series app."""
import json
from typing import Union, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, View, TemplateView
from django.views.generic import ListView

from series.forms import SearchSeriesForm
from series.models import APIShow
from tmdb.shortcuts import search_shows, retrieve_show, retrieve_season


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
    """Result page after a search by user."""

    template = 'series/search_results.html'

    def get(self, request, term: str):
        shows = search_shows(term)
        return render(
            template_name='series/search_results.html',
            request=request,
            context={'shows_list': shows, 'search_term': term}
        )


class ShowDetailsView(View):
    """Details of a show."""

    template = 'series/show_details.html'

    def get(self, request, id: int):
        show = retrieve_show(id)
        api_show: Optional[APIShow] = APIShow.objects.filter(pk=id).first()

        context = {
            'show': show,
            'user': request.user,
            'seasons_range': range(1, show.number_of_seasons + 1),
        }

        # Retrieve the current season, if specified in the query string
        season_number = request.GET.get('season')
        if season_number:
            season = retrieve_season(id, number=season_number)
        else:
            season = None
        context['season'] = season

        # Retrieve the number of followers and whether the user follows
        # this show.
        if api_show is not None:
            num_followers = api_show.num_followers
            follows = api_show.is_followed_by(request.user)
        else:
            num_followers = 0
            follows = False
        context['num_followers'] = num_followers
        context['follows'] = follows

        return render(
            template_name='series/show_details.html',
            request=request,
            context=context,
        )


class FollowedSeriesView(LoginRequiredMixin, ListView):
    """Page to display the followed series of a user."""

    template_name = 'series/followed_series.html'
    context_object_name = 'followed_series_list'

    def get_queryset(self):
        return APIShow.objects.filter(followers=self.request.user)


class APILoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        """Return a 401 Unauthorized error (JSON) if no credentials were passed.

        The default behavior would have been to redirect to the login page
        or return an HTML 403 response.
        """
        return HttpResponse(
            status=401,
            content_type='application/json',
            content=json.dumps({'error': 'Credentials not provided.'})
        )


class APISubscribe(APILoginRequiredMixin, View):
    """View called when a user subscribes or unsubscribes to a new show."""

    def post(self, request, show_id: int):
        """Called when a POST request is made.

        Subscribe the user to the show: add them to the show's list of
        followers."""
        try:
            show = APIShow.objects.get(id=show_id)
        except APIShow.DoesNotExist:
            show = APIShow.objects.create_from_api(show_id)
        show.followers.add(request.user)
        return HttpResponse(200)

    def delete(self, request, show_id: int):
        """Called when a DELETE request is made.

        Unsubscribe the user from the show: removes them from the show's
        list of the followers."""
        show = APIShow.objects.filter(id=show_id).first()
        if show is not None:
            show.followers.remove(request.user)
        return HttpResponse(200)


class About(TemplateView):
    """View for the About page."""

    template_name = 'series/about.html'
