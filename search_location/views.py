from django.shortcuts import render
from users.models import Profile
from main_crud.models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from geopy.distance import geodesic
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderInsufficientPrivileges
from functools import lru_cache
import time
import os

# Obtenha a chave da variável de ambiente
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure o geolocator com sua chave de API do Google
geolocator = GoogleV3(api_key=GOOGLE_API_KEY, timeout=10)

@lru_cache(maxsize=1000)
def do_geocode(address, geolocator, attempt=1, max_attempts=3):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
            return do_geocode(address, geolocator, attempt=attempt+1)
        raise

@login_required
def search_nearby_users(request):
    if request.method == 'GET':
        address = request.GET.get('address')
        max_distance_str = request.GET.get('max_distance', '10').strip()
        max_distance = float(max_distance_str) if max_distance_str else 10.0

        try:
            location = do_geocode(address, geolocator)
            if location:
                user_location = (location.latitude, location.longitude)
                photographer_group = Group.objects.get(name='Photographer')
                profiles = Profile.objects.filter(username__groups=photographer_group)
                nearby_users = []

                for profile in profiles:
                    profile_location = do_geocode(profile.address, geolocator)
                    if profile_location:
                        profile_coords = (profile_location.latitude, profile_location.longitude)
                        distance = geodesic(user_location, profile_coords).km
                        if distance <= max_distance:
                            nearby_users.append((profile, distance))

                nearby_users.sort(key=lambda x: x[1])  # Sort by distance
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

    return render(request, 'searchUsers.html')
