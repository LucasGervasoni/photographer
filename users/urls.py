from django.urls import path
from users.views import login, register, registerEditor, logout
from .views import ServicesCreateArtists, ProfileUpdate, CreateEditor
urlpatterns = [
    #Authentication
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('registerEditor/', registerEditor, name='registerEditor'),
    #Create
    path('create/photographer', ServicesCreateArtists.as_view(), name='create__artists'),
    path('create/editor', CreateEditor.as_view(), name='createEditor'),
    #Update
    path('update/artists/<int:pk>', ProfileUpdate.as_view(), name='updateArtists'),
]