from django.urls import path
from apps.search_location.views import SearchNearbyUsersView

urlpatterns = [
    path('search/', SearchNearbyUsersView.as_view(), name='search_nearby_users'),
]
