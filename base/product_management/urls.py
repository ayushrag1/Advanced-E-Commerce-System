from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'order', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', views.HealthCheck.as_view(), name='home'),
    path('', include(router.urls))
]
