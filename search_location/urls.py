from django.urls import path
from .views import search_nearby_users

urlpatterns = [
    path('search/', search_nearby_users, name='search_nearby_users'),
]
