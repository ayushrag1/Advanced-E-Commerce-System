import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr="iexact")  # Case-insensitive filter
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = django_filters.BooleanFilter(field_name="stock", lookup_expr="gt", method="filter_stock")

    def filter_stock(self, queryset, name, value):
        """Filter products by stock availability."""
        if value:  # True → in stock
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)  # False → out of stock

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "in_stock"]
