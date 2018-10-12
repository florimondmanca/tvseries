from django.urls import path

from series import views

urlpatterns = [
    path('', views.SearchSeriesView.as_view(), name='search_series'),
]
