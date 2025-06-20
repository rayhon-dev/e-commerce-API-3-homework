from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)
    subtotal = serializers.SerializerMethodField()
    shipping_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    tracking_number = serializers.CharField(read_only=True)


    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'created_time',
            'updated_time',
            'status',
            'shipping_address',
            'notes',
            'items',
            'subtotal',
            'shipping_fee',
            'total',
            'tracking_number'
        ]

    def get_subtotal(self, obj):
        return round(sum(item.price * item.quantity for item in obj.items.all()), 2)

    def create(self, validated_data):
        from cart.models import Cart, CartItem
        from .models import OrderItem

        user = self.context['request'].user
        shipping_address = validated_data.pop('shipping_address')
        notes = validated_data.pop('notes', '')

        cart = Cart.objects.filter(user=user).first()
        if not cart or cart.items.count() == 0:
            raise serializers.ValidationError("Savat bo‘sh.")

        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            notes=notes,
        )

        shipping_fee = 5
        total = 0
        count = 0

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total += item.product.price * item.quantity
            count += item.quantity

        order.total = total + shipping_fee
        order.shipping_fee = shipping_fee
        order.items_count = count
        order.save()

        cart.items.all().delete()
        cart.total = 0
        cart.items_count = 0
        cart.save()

        return order
