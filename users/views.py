from django.views.generic import CreateView, UpdateView

from .forms import SignUpForm
from .models import User


class SignUpView(CreateView):
    """Page to signup a new user."""
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = '/'

class ProfileView(UpdateView):
    """Page to view the current user profile."""
    model = User
    template_name = 'users/profile.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'avatar']

    def get_object(self, queryset=None):
        return self.request.user