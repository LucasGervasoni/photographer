from django.urls import path
from .views import uploadPage, listImages, UploadList

urlpatterns = [
    path('upload/', uploadPage, name="upload"),
    path('upload/lists', UploadList.as_view(), name="uploadLists"),
    path('upload/lists/<int:id>', listImages, name="listImages"),
]