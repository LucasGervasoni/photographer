from django.urls import path
from .views import ServicesCreateArtists, ServicesCreateOrders, ServicesListArtists,ServicesListOrders,UserPageOrders

urlpatterns = [
  path('services/create/artists', ServicesCreateArtists.as_view(), name='create_artists'),
  path('services/create/orders', ServicesCreateOrders.as_view(), name='create_orders'),
  path('services/list/artists', ServicesListArtists.as_view(), name='list__artists'),
  path('services/list/orders', ServicesListOrders.as_view(), name='list__orders'),
  path('orders/', UserPageOrders.as_view(), name='user__orders--page'),
 ]