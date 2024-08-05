from django.urls import path
from .views import  UploadList

urlpatterns = [
    path('upload/lists', UploadList.as_view(), name="uploadLists"),
]