from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from api.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

from author.models import Author
from book.models import Book
from order.models import Order
from django.contrib.auth.models import User

from api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Order.objects.all()
        else:
            user_id = self.request.user.id
            queryset = Order.objects.filter(user_id=user_id)
        return queryset
