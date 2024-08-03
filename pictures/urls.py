from django.urls import path
from .views import uploadPage, ListImages

urlpatterns = [
    path('upload/', uploadPage, name="upload"),
    path('list/images', ListImages.as_view(), name="listImages"),
]