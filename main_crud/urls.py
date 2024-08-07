from django.urls import path
from .views import UserPageOrders, UpdateOrderStatusView

urlpatterns = [
  #LIST
  path('orders/', UserPageOrders.as_view(), name='userOrders--page'),
  path('orders/<int:pk>/update_status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
 ]