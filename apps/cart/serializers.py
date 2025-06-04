from rest_framework import serializers
from products.models import Product
from .models import Cart, CartItem

class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'thumbnail']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['items', 'total', 'items_count']

