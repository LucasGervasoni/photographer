from django.urls import path
from .views import  OrderImageListView, OrderImageUploadView

urlpatterns = [
    path('orders/<int:pk>/upload/', OrderImageUploadView.as_view(), name='order_image_upload'),
    path('orders/<int:pk>/images/', OrderImageListView.as_view(), name='order_images'),
]
