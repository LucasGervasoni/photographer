from django.shortcuts import render
from users.models import Profile
from main_crud.models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from geopy.distance import geodesic
# Imports the `geodesic` function from the `geopy` library, which is used to calculate the distance between two geographic points.
from geopy.geocoders import Nominatim
# Imports the `Nominatim` geocoder from the `geopy` library, used to convert addresses into geographic coordinates.
from geopy.exc import GeocoderTimedOut
# Imports the `GeocoderTimedOut` exception from the `geopy` library, used to handle timeout errors during geocoding.
from functools import lru_cache
# Imports the `lru_cache` decorator from the `functools` library, which is used to cache the results of functions, in this case, the geocoding.
import time
# Imports the `time` module, which is used to add delays (sleep) between geocoding attempts, helping to avoid overloading the service.


# Function with retry e caching
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
        # Handle max_distance by providing a default value if it's not set or is invalid
        max_distance_str = request.GET.get('max_distance', '10').strip()
        if max_distance_str:
            try:
                max_distance = float(max_distance_str)
            except ValueError:
                max_distance = 10.0  # Default to 10 km if conversion fails
        else:
            max_distance = 10.0  # Default to 10 km if max_distance is empty

        # Configure the geolocator with a longer timeout time
        geolocator = Nominatim(user_agent="geoapi", timeout=10)

        # Use the geocoding function with retry and caching
        location = do_geocode(address, geolocator)
        
        if location:
            user_location = (location.latitude, location.longitude)
            # Get the group for photographers
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

            # Sort users by proximity
            nearby_users.sort(key=lambda x: x[1])  # Sort by distance
            
            # Add pagination, 10 users per page
            paginator = Paginator(nearby_users, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'searchUsers.html', {'page_obj': page_obj,'address': address})
        
        return render(request, 'searchUsers.html', {'error': 'Invalid address or geocoding service timed out. Please try again later.'})

    return render(request, 'searchUsers.html')
