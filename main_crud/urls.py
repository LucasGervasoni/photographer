from django.urls import path
from .views import  ServicesCreateOrders,ServicesUpdateOrders, ServicesDeleteOrders, ServicesListOrders, UserPageOrders, ServicesListArtists, ServicesDeleteArtists, HomeListOrders

urlpatterns = [
  #CREATE
  path('create/orders', ServicesCreateOrders.as_view(), name='createOrders'),
  
  #UPDATE
  path('update/orders/<int:pk>', ServicesUpdateOrders.as_view(), name='updateOrders'),
  
  #LIST
  path('list/artists', ServicesListArtists.as_view(), name='listArtists'),
  path('list/orders', ServicesListOrders.as_view(), name='listOrders'),
  path('home/orders', HomeListOrders.as_view(), name='homeOrders'),
  path('orders/', UserPageOrders.as_view(), name='userOrders--page'),
  
  #DELETE
  path('delete/orders/<int:pk>', ServicesDeleteOrders.as_view(), name='deleteOrders'),
  path('delete/artists/<int:pk>', ServicesDeleteArtists.as_view(), name='deleteArtists'),
 ]