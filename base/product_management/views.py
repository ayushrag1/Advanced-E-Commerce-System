from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


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
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category")
    lookup_field = 'name'
