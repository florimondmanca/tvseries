from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.SearchSeriesView.as_view(), name='search_series'),
    path('search/<str:term>', views.SearchResultsView.as_view(), name='search_results'),
    path('tvshow/<str:id>', views.ShowDetailsView.as_view(), name='show_details'),
    path('tvshow/followed/', views.FollowedSeriesView.as_view(), name='followed_series')
]
