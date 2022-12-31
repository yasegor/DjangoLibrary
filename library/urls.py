from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views
from library.settings import DEBUG, MEDIA_URL, MEDIA_ROOT, STATIC_URL

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('authors/', include('author.urls')),
    path('books/', include('book.urls')),
    path('orders/', include('order.urls')),
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
