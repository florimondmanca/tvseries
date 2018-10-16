from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.SearchSeriesView.as_view(), name='search_series'),
    path('search/<str:term>', views.SearchResultsView.as_view(), name='search_results')
]
