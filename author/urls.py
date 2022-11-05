from django.urls import path

from . import views

# urlpatterns = [
#     path('', views.all_authors, name="author_list"),
#     path('create/', views.create_author, name="author_create"),
#     path('author/<int:id>/', views.author_detail, name="author_detail"),
#     path('update/<int:id>/', views.author_update, name="author_update"),
# ]

urlpatterns = [
    path('', views.all_authors, name="author_list"),
    path('create/', views.author_form, name="author_create"),
    path('<int:id>/', views.author_detail, name="author_detail"),
    path('update/<int:id>/', views.author_form, name="author_update"),
    path('delete/<int:id>/', views.author_delete, name="author_delete"),
]
