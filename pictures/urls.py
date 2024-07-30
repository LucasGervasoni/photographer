from django.urls import path
from .views import uploadPage

urlpatterns = [
    path('upload/', uploadPage, name="upload")
]