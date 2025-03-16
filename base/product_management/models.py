from django.db.models import (CASCADE, CharField, CheckConstraint,
                              DateTimeField, DecimalField, F, ForeignKey,
                              IntegerChoices, ManyToManyField, Model,
                              PositiveIntegerField, Q, Sum, TextField,
                              UniqueConstraint)

from base.user_profile.models import UserProfile


class Category(Model):
    name = CharField(max_length=255)
    description = TextField()

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = PositiveIntegerField(null=False, default=0)
    description = TextField(null=True, blank=True)
    category = ForeignKey(Category, on_delete=CASCADE, related_name="products")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(Model):
    class OrderStatus(IntegerChoices):
        PENDING = 0, 'Pending'
        SHIPPED = 1, 'Shipped'
        DELIVERED = 2, 'Delivered'

    user = ForeignKey(UserProfile, on_delete=CASCADE, related_name='orders')
    products = ManyToManyField(Product, through='OrderItem')
    status = PositiveIntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        """Optimized total price calculation using aggregation"""
        return self.order_items.aggregate(
            total=Sum(F("quantity") * F("product__price"))
        ).get("total") or 0.0

    def __str__(self):
        return f"Order #{self.id} - {self.user.user_id} - {self.get_status_display()} - ${self.total_price}"


class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='order_items')
    product = ForeignKey(Product, on_delete=CASCADE, related_name="ordered_product")
    quantity = PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(quantity__gte=1), name="quantity_gte_1"),
            UniqueConstraint(fields=["order", "product"], name="unique_order_product"),
        ]

    @property
    def order_amount(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order #{self.order.id}"
