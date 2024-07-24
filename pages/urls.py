from django.urls import path
from .views import ServicesView, UserUploadPage

urlpatterns = [
  path('services/', ServicesView.as_view(), name='services'),
  path('upload/', UserUploadPage.as_view(), name='user__upload--page'),
]