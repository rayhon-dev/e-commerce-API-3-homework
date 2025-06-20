from django.db import models
from common.models import BaseModel
from users.models import User


class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='product_thumbnails/')
    category =models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    average_rating = models.FloatField(default=0.0)
    likes_count =models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')











