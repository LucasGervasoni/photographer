from django.urls import path
from users.views import login, register, logout
from .views import ServicesCreateArtists, ProfileUpdate

urlpatterns = [
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    #Create
    path('services/create/artists', ServicesCreateArtists.as_view(), name='create__artists'),
    #Update
    path('services/update/artists/<int:pk>', ProfileUpdate.as_view(), name='update__artists'),
]