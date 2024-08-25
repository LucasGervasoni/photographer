from django.urls import path
from apps.pages.views import Support

urlpatterns = [
  path('support/', Support.as_view(), name='support'),
 ]