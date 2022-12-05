from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('auth.urls')),
    path('authors/', include('author.urls')),
    path('books/', include('book.urls')),
    path('orders/', include('order.urls')),
]
