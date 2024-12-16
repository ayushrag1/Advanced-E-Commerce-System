from django.urls import path

from . import views

url_pattern = [
    path("products/", views.ProductManagement.as_view()),
    path("category/", views.CategoryManagement.as_view()),
    path("shopping/", views.OrderCartOperation.as_view()),
]
