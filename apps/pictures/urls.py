from django.urls import path
from apps.pictures.views import  OrderImageListView, OrderImageUploadView, OrderImageDownloadView, PhotographerImageUploadView, FilesListView, FileDeleteView, LogListView, LogDeleteView

urlpatterns = [
    #UPLOAD
    path('orders/<int:pk>/upload/', OrderImageUploadView.as_view(), name='order_image_upload'),
    path('orders/<int:pk>/upload_photographer/', PhotographerImageUploadView.as_view(), name='order_image_upload_photographer'),
    #LIST
    path('orders/<int:pk>/images/', OrderImageListView.as_view(), name='order_images'),
    path('files/', FilesListView.as_view(), name='list_files'),
    path('files/', FilesListView.as_view(), name='list_files'),
    path('logs/', LogListView.as_view(), name='list_logs'),
    #DELETE
    path('files/<int:pk>/delete', FileDeleteView.as_view(), name='delete_files'),
    path('logs/<int:pk>/delete', LogDeleteView.as_view(), name='delete_logs'),
    #DOWNLOAD
    path('orders/<int:pk>/download/', OrderImageDownloadView.as_view(), name='order_image_download'),
]
