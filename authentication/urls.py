from django.urls import path
from django.views.generic import TemplateView

from . import views
from . import utils

urlpatterns = [
    # path('', views.user_info, name="user_info"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('activate/<uidb64>/<token>/', utils.EmailVerify.as_view(), name='verify_email'),
]
