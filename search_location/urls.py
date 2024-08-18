from django.urls import path
from .views import SearchNearbyUsersView

urlpatterns = [
    path('search/', SearchNearbyUsersView.as_view(), name='search_nearby_users'),
]
