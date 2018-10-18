from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .forms import SignUpForm
from .models import User
from series.models import APIShow
from django.http import HttpResponse, HttpResponseRedirect


class SignUpView(CreateView):
    """Page to signup a new user."""
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = '/'

class FavedSeriesView(LoginRequiredMixin, ListView):
    template_name = "users/followed_series.html"
    context_object_name = 'faved_series_list'

    login_url = 'login/'
    redirect_field_name = ''

    def get_queryset(self):
        # user = self.request.user
        # if self.request.user.is_anonymous:#is_authenticated():
        #     # return None
        #     return redirect('/accounts/login')#None#HttpResponseRedirect('accounts/login')
        # else:
            return APIShow.objects.filter(followers=self.request.user)

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


