from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect

from .forms import SignUpForm
from .models import User


class SignUpView(CreateView):
    """Page to signup a new user."""
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = '/'


class ProfileView(LoginRequiredMixin, UpdateView):
    """Page to view the current user profile."""
    model = User
    template_name = 'users/profile.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
