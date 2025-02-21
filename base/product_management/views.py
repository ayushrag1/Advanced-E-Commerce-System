from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer


class HealthCheck(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            data={"message": "Health Check True! From Product Management"},
            status=status.HTTP_200_OK
        )


class CategoryView(RetrieveUpdateDestroyAPIView, ListCreateAPIView):
    permission_classes = [AllowAny | IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        name = kwargs.get('name')
        if name:
            # If 'name' is provided, return the specific category
            try:
                category = Category.objects.get(name=name)
                serializer = self.serializer_class(category)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response(
                    {"detail": f"Category with name '{name}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # If no 'name' is provided, return all categories
            categories = Category.objects.all()
            serializer = self.serializer_class(categories, many=True)
            return Response(serializer.data)
