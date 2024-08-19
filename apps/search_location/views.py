from django.shortcuts import render  # For rendering HTML templates
from django.urls import reverse_lazy
from django.views import View
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from apps.users.models import CustomUser
from django.core.paginator import Paginator  # For paginating querysets
from django.contrib.auth.models import Group  # To work with user groups
from geopy.distance import geodesic  # For calculating distances between geographic coordinates
from geopy.geocoders import GoogleV3  # Google geocoding service
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderInsufficientPrivileges  # Exceptions for handling geocoding errors
from functools import lru_cache  # For caching results of expensive function calls
import time  # For sleep and time-related functions
import os  # For interacting with the operating system

# Get the API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure the geolocator with your Google API key
geolocator = GoogleV3(api_key=GOOGLE_API_KEY, timeout=10)

@lru_cache(maxsize=1000)
def do_geocode(address, geolocator, attempt=1, max_attempts=3):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            time.sleep(1)  # Wait for 1 second before retrying
            return do_geocode(address, geolocator, attempt=attempt+1)
        raise

class SearchNearbyUsersView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = ['Admin']
    login_url = reverse_lazy('login')

    def get(self, request):
        address = request.GET.get('address')
        max_distance_str = request.GET.get('max_distance', '10').strip()
        max_distance = float(max_distance_str) if max_distance_str else 10.0

        try:
            location = do_geocode(address, geolocator)
            if location:
                user_location = (location.latitude, location.longitude)
                photographer_group = Group.objects.get(name='Photographer')
                profiles = CustomUser.objects.filter(groups=photographer_group)  # Note: Assuming CustomUser has address field
                nearby_users = []

                for profile in profiles:
                    profile_location = do_geocode(profile.address, geolocator)
                    if profile_location:
                        profile_coords = (profile_location.latitude, profile_location.longitude)
                        distance = geodesic(user_location, profile_coords).km
                        if distance <= max_distance:
                            nearby_users.append((profile, distance))

                nearby_users.sort(key=lambda x: x[1])
                paginator = Paginator(nearby_users, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                return render(request, 'searchUsers.html', {'page_obj': page_obj, 'address': address})

            return render(request, 'searchUsers.html', {'error': 'Invalid address or geocoding service timed out. Please try again later.'})
        
        except GeocoderQuotaExceeded:
            return render(request, 'searchUsers.html', {'error': 'Geocoding service quota exceeded. Please try again later.'})
        except GeocoderInsufficientPrivileges:
            return render(request, 'searchUsers.html', {'error': 'Insufficient privileges to use the geocoding service. Please contact support.'})
        except Exception as e:
            return render(request, 'searchUsers.html', {'error': f'An unexpected error occurred: {str(e)}'})