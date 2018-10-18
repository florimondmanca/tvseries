from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm
from .models import User
from series.models import APIShow


class SignUpView(CreateView):
    """Page to signup a new user."""
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = '/'


class FavedSeriesView(LoginRequiredMixin, ListView):
    template_name = "users/followed_series.html"
    context_object_name = 'faved_series_list'

    login_url = '/accounts/login/'
    redirect_field_name = ''

    def get_queryset(self):
        return APIShow.objects.filter(followers=self.request.user)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        return redirect_to
