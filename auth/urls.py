from django.urls import path

from . import views

urlpatterns = [
    # path('', views.user_info, name="user_info"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout")
]
