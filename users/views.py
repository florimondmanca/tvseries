from django.views.generic import CreateView, ListView

from .forms import SignUpForm
from .models import User
from series.models import APIShow
from django.http import HttpResponse


class SignUpView(CreateView):
    """Page to signup a new user."""
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = '/'


class UserProfile(ListView):
    template_name = "users/followed_series.html"
    context_object_name = 'faved_series_list'
    # model = APIShow

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        else:
            return user.favorites.all()

    # def get_queryset(self):
    #     username = self.request.GET.get('username',None)
    #     user = None
    #     if username:
    #         try:
    #             user = User.objects.get(username=username)
    #         except (User.DoesNotExist, User.MultipleObjectsReturned):
    #             pass
    #     if user:
    #         return User.objects.filter(user=user)
    #     return User.objects.none()


