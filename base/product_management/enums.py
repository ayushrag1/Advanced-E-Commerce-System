from enum import IntEnum


class OrderStatus(IntEnum):
    PENDING = 0
    SHIPPED = 1
    DELIVERED = 2
