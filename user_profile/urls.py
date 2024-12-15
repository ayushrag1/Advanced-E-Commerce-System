from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('register/', views.CreateUserProfile.as_view(), name='register'),
    path('manage/', views.ManageUserProfile.as_view(), name='manage'),
    path(
        'manage/user_id/<int:user_id>/',
        views.ManageUserProfile.as_view(),
        name='user-profile'
    ),
    path('login/', views.Login.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
