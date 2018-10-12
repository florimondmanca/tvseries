from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from .models import User
from .forms import SignUpForm
import os

# Create your views here.

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = os.path.join('series', 'signup.html')