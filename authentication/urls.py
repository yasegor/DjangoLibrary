from django.urls import path, include

from . import views
from . import utils

urlpatterns = [
    path('profile/', views.profile_view, name="profile"),
    path('profile/update/<int:id>/', views.profile_update, name='profile_update'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name="logout"),
    path('activate/<uidb64>/<token>/', utils.EmailVerify.as_view(), name='verify_email'),
    path('get-token/', views.create_token, name='get_token')
]
