from django.urls import include, re_path

from .product_management.urls import urlpatterns as products_urls
from .user_profile.urls import urlpatterns as user_profile_urls

url_patterns = [
    re_path(r'^auth/', include(user_profile_urls)),
    re_path(r'^product/', include(products_urls)),
]
