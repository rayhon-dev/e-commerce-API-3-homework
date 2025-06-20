from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from products.models import Product
from .models import CartItem
from decimal import Decimal
from rest_framework.views import APIView




class CartListCreateView(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)

        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'success': False, 'error': 'Mahsulot IDsi kerak'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'success': False, 'error': 'Bunday mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'subtotal': product.price * Decimal(quantity)}
        )
        if not item_created:
            cart_item.quantity += quantity
            cart_item.subtotal = cart_item.quantity * product.price
            cart_item.save()

        items = CartItem.objects.filter(cart=cart)
        cart.total = sum(item.subtotal for item in items)
        cart.items_count = sum(item.quantity for item in items)
        cart.save()

        serializer = self.get_serializer(cart)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)



class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"success": False, "error": "Cart topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = CartItem.objects.get(cart=cart, product__id=product_id)
        except CartItem.DoesNotExist:
            return Response({"success": False, "error": "CartItem topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()

        # cart total va count yangilash
        items = CartItem.objects.filter(cart=cart)
        cart.total = sum(i.subtotal for i in items)
        cart.items_count = sum(i.quantity for i in items)
        cart.save()

        serializer = CartSerializer(cart)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
