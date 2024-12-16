from django.db import models

from user_profile.models import UserProfile

from .enums import OrderStatus


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def with_category(self):
        return self.select_related('category')


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db).select_related('category')


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True,)
    price = models.PositiveIntegerField(null=False)
    stock = models.PositiveIntegerField(null=False)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        null=False,
    )

    objects = ProductManager()

    def __str__(self):
        return self.name


class Orders(models.Model):
    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.SET_NULL,
        null=True
    )
    total_price = models.PositiveIntegerField(default=0)
    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    products = models.ManyToManyField(
        to=Product,
        through='OrderProduct',  # Use the through model
        related_name='orders'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=False
    )

    def __str__(self):
        return f"Order {self.id} - {self.user} - {self.get_status_display()}"


class OrderProduct(models.Model):
    order = models.ForeignKey(
        to=Orders,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Order {self.order.id}"
