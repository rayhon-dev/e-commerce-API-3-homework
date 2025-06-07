from rest_framework import generics
from common.pagination import CustomPagination
from .serializers import CartSerializer
from .models import Cart, CartItem


class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = CustomPagination


class CartDeleteView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'pk'
