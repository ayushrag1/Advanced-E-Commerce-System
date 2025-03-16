from django.contrib import admin
from django.db.models import F, Sum

from .models import Category, Order, OrderItem, Product


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Allows adding extra product rows
    min_num = 1  # Ensure at least one product is added
    fields = ('product', 'quantity')  # Fields shown in admin panel


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'id')  # Search orders by user or order ID
    readonly_fields = ('total_price',)  # Ensure total_price is not editable
    inlines = [OrderItemInline]  # Add inline OrderItem management

    def total_price(self, obj):
        """Calculate total price dynamically for admin display."""
        total = obj.order_items.aggregate(
            total=Sum(F("quantity") * F("product__price"))
        )["total"]
        return total or 0

    total_price.short_description = "Total Price (INR)"  # Rename column header


# Register models in Django Admin
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
