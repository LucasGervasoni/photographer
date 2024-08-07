from django.urls import path
from .views import  OrderImageListView, OrderImageUploadView, OrderImageDownloadView, PhotographerImageUploadView

urlpatterns = [
    path('orders/<int:pk>/upload/', OrderImageUploadView.as_view(), name='order_image_upload'),
    path('orders/<int:pk>/upload_photographer/', PhotographerImageUploadView.as_view(), name='order_image_upload_photographer'),
    path('orders/<int:pk>/images/', OrderImageListView.as_view(), name='order_images'),
    path('orders/<int:pk>/download/', OrderImageDownloadView.as_view(), name='order_image_download'),
]
