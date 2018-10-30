"""Users views.

Docs on LoginView and LogoutView:
https://docs.djangoproject.com/fr/2.1/topics/auth/default/#django.contrib.auth.views.LoginView
"""

from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

login_view_config = {
    'template_name': 'users/login.html',
}
logout_view_config = {
    'template_name': 'users/logged_out.html',
}

urlpatterns = [
    path('login/', views.OwnLoginView.as_view(**login_view_config), name='login'),
    path('logout/', LogoutView.as_view(**logout_view_config), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]
