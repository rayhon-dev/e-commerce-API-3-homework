from django.db import models
from users.models import User
from products.models import Product
from decimal import Decimal


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    items_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"


    def save(self, *args, **kwargs):
        self.quantity = int(self.quantity)
        self.subtotal = self.product.price * Decimal(self.quantity)
        super().save(*args, **kwargs)

