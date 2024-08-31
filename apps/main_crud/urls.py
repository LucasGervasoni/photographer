from django.urls import path
from apps.main_crud.views import UserPageOrders, UpdateOrderStatusView,OrderCreateView,AdminListOrders,OrderUpdateView, OrderDeleteView, AssignOrderEditorView

urlpatterns = [
  #CREATE
  path('orders/new/', OrderCreateView.as_view(), name='order-create'),
  #LIST
  path('orders/', UserPageOrders.as_view(), name='userOrders--page'),
  path('orders/admin', AdminListOrders.as_view(), name='adminOrders--page'),
  #UPDATE
  path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order-update'),
  path('orders/<int:pk>/update_status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
  path('orders/<int:order_id>/assign-editor/', AssignOrderEditorView.as_view(), name='assign_order_editor'),
  #DELETE
  path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
 ]