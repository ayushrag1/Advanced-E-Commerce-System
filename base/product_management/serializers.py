from rest_framework import serializers, status
from rest_framework.exceptions import NotFound

from ..user_profile.serializer import UserProfileSerializer
from .models import Category, Order, OrderItem, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Product
        exclude = ["category"]

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

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category_name', None)  # Fix here
        if category_name:
            category_obj = Category.objects.filter(name=category_name).first()
            if not category_obj:
                raise NotFound(
                    detail={"message": f"Category with name `{category_name}` is not present"},
                    code=status.HTTP_404_NOT_FOUND
                )
            validated_data['category'] = category_obj

        return super().update(instance, validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    order_amount = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "order_amount")


class OrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Order
        exclude = ["products"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["status"] = instance.get_status_display()
        return representation
