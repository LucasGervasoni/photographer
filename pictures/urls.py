from django.urls import path
from .views import uploadPage, UploadList

urlpatterns = [
    path('upload/', uploadPage, name="upload"),
    path('upload/lists', UploadList.as_view(), name="uploadLists"),
]