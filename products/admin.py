from django.contrib import admin

from .models import Category, OrderProduct, Orders, Product


# Register Category model in admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    fieldsets = (
        ('Product Category Details', {
            'fields': ('name', 'description')
        }),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    ordering = ('-price', 'stock')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Category', {
            'fields': ('category',)
        }),
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at', 'updated_at')


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_per_unit')


# Register the models with their respective ModelAdmin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Orders, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
