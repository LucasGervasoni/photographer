from django.urls import path
from .views import  ServicesCreateOrders,ServicesUpdateOrders, ServicesDeleteOrders, ServicesListOrders, UserPageOrders, ServicesListArtists

urlpatterns = [
  #CREATE
  path('services/create/orders', ServicesCreateOrders.as_view(), name='create_orders'),
  #UPDATE
  path('services/update/orders/<int:pk>', ServicesUpdateOrders.as_view(), name='update_orders'),
  #LIST
  path('services/list/artists', ServicesListArtists.as_view(), name='list__artists'),
  path('services/list/orders', ServicesListOrders.as_view(), name='list__orders'),
  path('orders/', UserPageOrders.as_view(), name='user__orders--page'),
  #DELETE
  path('services/delete/orders/<int:pk>', ServicesDeleteOrders.as_view(), name='delete_orders'),
 ]