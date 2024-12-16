from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Category, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    # Include category_name for both input and output
    category_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category_name']

    def _get_category_instance_by_name(self, category_name):
        """
        Retrieves the Category instance by its name or raises a ValidationError if not found.
        """
        if not category_name:
            raise serializers.ValidationError("Category name is required.")
        try:
            return Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                f"Category with name '{category_name}' not found."
            )

    def create(self, validated_data):
        # Extract and fetch the related category
        category_name = validated_data.pop('category_name')
        category = self._get_category_instance_by_name(category_name)

        # Create the Product instance
        return Product.objects.create(category=category, **validated_data)

    def update(self, instance, validated_data):
        # Extract and fetch the related category if provided
        category_name = validated_data.pop('category_name', None)
        if category_name:
            instance.category = self._get_category_instance_by_name(category_name)

        # Update the rest of the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Customizes the serialized output to include `category_name`.
        """
        representation = super().to_representation(instance)
        representation['category_name'] = instance.category.name  # Add category name
        return representation
