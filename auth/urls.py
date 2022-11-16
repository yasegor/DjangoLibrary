from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    # path('', views.user_info, name="user_info"),
    # path('login/', views.user_login, name="login"),
    path('register/', views.register_request, name="signup"),
    path('logout/', LogoutView.as_view(template_name=''), name="logout")
]
