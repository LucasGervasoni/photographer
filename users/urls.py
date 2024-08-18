from django.urls import path
from users.views import login, RegisterView, logout, UserListView, UserUpdateView, UserDeleteView
urlpatterns = [
    #Authentication
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    #LIST
    path('users/', UserListView.as_view(), name='listUsers'),
    #UPDATE
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='updateUser'),
    #DELETE
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='deleteUser'),
]