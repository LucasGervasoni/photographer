from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('pages.urls')),
        path('', include('users.urls')),
        path('', include('main_crud.urls')),
        path('', include('pictures.urls')),
        path('', include('search_location.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)