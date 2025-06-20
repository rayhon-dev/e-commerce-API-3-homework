from django.db import models
from django.utils import timezone
from common.models import BaseModel
from users.models import User
from products.models import Product
import random


def generate_order_number():
    today = timezone.now().strftime('%Y%m%d')
    last_order = Order.objects.filter(order_number__startswith=f'ORD-{today}').order_by('id').last()
    if last_order:
        last_id = int(last_order.order_number.split('-')[-1])
    else:
        last_id = 0
    return f'ORD-{today}-{last_id + 1:04d}'


class Order(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=30, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    items_count = models.PositiveIntegerField(default=0)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = generate_order_number()

        if not self.tracking_number:
            self.tracking_number = f"1Z{random.randint(10000000000000000000, 99999999999999999999)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
