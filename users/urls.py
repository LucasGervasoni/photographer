from django.urls import path
from users.views import login, register, logout
from .views import ServicesCreateArtists, ProfileUpdate

urlpatterns = [
    #Authentication
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    #Create
    path('create/artists', ServicesCreateArtists.as_view(), name='create__artists'),
    #Update
    path('update/artists/<int:pk>', ProfileUpdate.as_view(), name='updateArtists'),
]