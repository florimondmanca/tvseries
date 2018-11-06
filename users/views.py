from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

from .forms import SignUpForm
from .models import User


class SignUpView(UserPassesTestMixin, CreateView):
    """Page to signup a new user.
    Can only be accessed by non-logged users.
    """
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_success_url(self) -> str:
        return reverse('login')

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        return redirect('/')


class OwnLoginView(UserPassesTestMixin, LoginView):
    """Page to login.
    Can only be accessed by non-logged users.
    """

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        return redirect('/')


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
