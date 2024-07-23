from django.urls import path
from .views import LoginView, ServicesView, ServicesCreateArtists, ServicesCreateOrders, ServicesListArtists,ServicesListOrders, UserPageOrders, UserUploadPage

urlpatterns = [
  path('', LoginView.as_view(), name='login'),
  path('services/', ServicesView.as_view(), name='services'),
  path('services/create/artists', ServicesCreateArtists.as_view(), name='create_artists'),
  path('services/create/orders', ServicesCreateOrders.as_view(), name='create_orders'),
  path('services/list/artists', ServicesListArtists.as_view(), name='list__artists'),
  path('services/list/orders', ServicesListOrders.as_view(), name='list__orders'),
  path('orders/', UserPageOrders.as_view(), name='user__orders--page'),
  path('upload/', UserUploadPage.as_view(), name='user__upload--page'),
]