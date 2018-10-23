from django.views.generic import CreateView

from .forms import SignUpForm
from .models import User


class SignUpView(CreateView):
    """Page to signup a new user."""
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = '/'
