from django.urls import path
from apps.pictures.views import  OrderImageListView, OrderImageUploadView, OrderImageDownloadView, PhotographerImageUploadView, FilesListView, FileDeleteView, LogListView, LogDeleteView, CreateOrderImageGroupView, ToggleImageSelectionView

urlpatterns = [
    #UPLOAD
    path('orders/<int:pk>/upload/', OrderImageUploadView.as_view(), name='order_image_upload'),
    path('orders/<int:pk>/upload_photographer/', PhotographerImageUploadView.as_view(), name='order_image_upload_photographer'),
    path('order/<int:pk>/create-group/', CreateOrderImageGroupView.as_view(), name='create_order_image_group'),
    #LIST
    path('orders/<int:pk>/images/', OrderImageListView.as_view(), name='order_images'),
    path('files/', FilesListView.as_view(), name='list_files'),
    path('logs/', LogListView.as_view(), name='list_logs'),
    #DELETE
    path('files/<int:pk>/delete', FileDeleteView.as_view(), name='delete_files'),
    path('logs/<int:pk>/delete', LogDeleteView.as_view(), name='delete_logs'),
    #DOWNLOAD
    path('orders/<int:pk>/generate-zip/', OrderImageDownloadView.as_view(), name='order_image_download'),
    path('toggle-image-selection/<int:image_id>/', ToggleImageSelectionView.as_view(), name='toggle_image_selection')
]
