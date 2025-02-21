from rest_framework import serializers, status
from rest_framework.exceptions import NotFound

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Product
        fields = ("name", "price", "description", "category_name")

    def create(self, validated_data):
        category_name = validated_data.pop('category_name', None)
        if category_name:
            category_obj = Category.objects.filter(name=category_name).first()
            if not category_obj:
                raise NotFound(
                    detail={
                        "message": f"Category with name `{category_name}` is not present",
                    },
                    code=status.HTTP_404_NOT_FOUND
                )
            validated_data['category'] = category_obj
        return super().create(validated_data)
