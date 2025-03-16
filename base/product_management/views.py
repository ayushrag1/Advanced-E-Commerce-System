from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter
from .models import Category, Order, Product
from .paginations import ProductListPagination
from .serializers import CategorySerializer, OrderSerializer, ProductSerializer


class HealthCheck(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            data={"message": "Health Check True! From Product Management"},
            status=status.HTTP_200_OK
        )


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category")
    lookup_field = 'name'
    pagination_class = ProductListPagination  # Use custom pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ["price", "stock"]  # Allow sorting by price & stock
    ordering = ["-created_at"]  # Default sorting (newest first)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    queryset = orders = (
        Order.objects
        .select_related("user")
        .prefetch_related(
            "order_items__product__category"  # Prefetch product & category in a single query
        )
    )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()
