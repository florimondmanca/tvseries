"""Users views."""

from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('users/<int:pk>/', views.UserProfile.as_view(), name='faved_series'),
]
