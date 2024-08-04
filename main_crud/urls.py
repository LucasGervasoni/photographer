from django.urls import path
from .views import UserPageOrders

urlpatterns = [
  #LIST
  path('orders/', UserPageOrders.as_view(), name='userOrders--page'),
 ]