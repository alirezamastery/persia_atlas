import uuid

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='shop_orders')

    items = models.ManyToManyField('shop.Variant', through='shop.OrderItem')

    price_sum = models.PositiveBigIntegerField()
    is_canceled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.created_at}'


class OrderItem(models.Model):
    order = models.ForeignKey('shop.Order', on_delete=models.PROTECT)
    item = models.ForeignKey('shop.Variant', on_delete=models.PROTECT)

    price = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'item'],
                name='unique_order_item'
            )
        ]
