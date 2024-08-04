from django.urls import path
from users.views import login, register,logout
urlpatterns = [
    #Authentication
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]