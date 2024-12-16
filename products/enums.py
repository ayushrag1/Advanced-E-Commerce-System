from django.db import models


class OrderStatus(models.IntegerChoices):
    PENDING = 0, 'Pending'
    SHIPPED = 1, 'Shipped'
    DELIVERED = 2, 'Delivered'
