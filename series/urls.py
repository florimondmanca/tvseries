from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchSeriesView.as_view(), name='search_series'),
]
