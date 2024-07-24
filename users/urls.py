from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserCreate

urlpatterns = [
    path('', auth_views.LoginView.as_view(
            template_name='login_page.html'
        ), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', UserCreate.as_view(), name='register'),
    # path('update-data/', ProfileUpdate.as_view(), name='update__data'),
]