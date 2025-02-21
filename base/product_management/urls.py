from django.urls import path

from . import views

urlpatterns = [
    path('', views.HealthCheck.as_view(), name='home'),
    path('category/', views.CategoryView.as_view(), name='list-category'),
    path('category/<str:name>/', views.CategoryView.as_view(), name='category-detail'),
]
