from django.urls import path, include, re_path
from rest_framework import routers

from library.settings import DEBUG
from api.views import *

if DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path(r'api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
