from django.urls import path
from .views import uploadPage, listImages

urlpatterns = [
    path('upload/', uploadPage, name="upload"),
    path('list/images', listImages, name="listImages"),
]