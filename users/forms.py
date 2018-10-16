from django.contrib.auth.forms import UserCreationForm

from users.models import User


class SignUpForm(UserCreationForm):
    """Form for new user to sign up."""

    class Meta(UserCreationForm.Meta):
        model = User
