from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_orders, name="order_list"),
    path('create/', views.create_order, name="order_create"),
    path('detail/<int:id>/', views.order_detail, name="order_detail"),
    path('update/<int:id>/', views.order_update, name="order_update"),
]
