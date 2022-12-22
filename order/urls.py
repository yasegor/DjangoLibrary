from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_orders, name="order_list"),
    path('create/', views.create_order, name="order_create"),
    path('update/<int:id>/', views.order_update, name="order_update"),
    path('delete/<int:id>/', views.order_delete, name="order_delete"),
]
