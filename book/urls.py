from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_books, name="book_list"),
    path('create/', views.book_form, name="book_create"),
    path('<int:id>/', views.book_detail, name="book_detail"),
    path('update/<int:id>/', views.book_form, name="book_update"),
    path('delete/<int:id>/', views.book_delete, name="book_delete"),
]
