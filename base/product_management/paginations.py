from rest_framework.pagination import PageNumberPagination


class ProductListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"  # Allow users to modify page size
    max_page_size = 10
